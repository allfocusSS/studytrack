from html.parser import HTMLParser

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sessions.models import Session
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils.html import escape

User = get_user_model()

# Explicitly public synthetic test data, never browser/development credentials.
PUBLIC_PASSWORD = "Public-Test-Password-842!Quartz"


class ParsedPage(HTMLParser):
    def __init__(self, response):
        super().__init__()
        self.inputs = []
        self.labels = []
        self.forms = []
        self.current_form = None
        self.feed(response.content.decode())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "form":
            self.current_form = {"attrs": attrs, "inputs": []}
            self.forms.append(self.current_form)
        elif tag == "input":
            self.inputs.append(attrs)
            if self.current_form is not None:
                self.current_form["inputs"].append(attrs)
        elif tag == "label":
            self.labels.append(attrs.get("for"))

    def handle_endtag(self, tag):
        if tag == "form":
            self.current_form = None


class AccountAssertions:
    def assert_password_inputs_empty(self, response):
        passwords = [field for field in ParsedPage(response).inputs if field.get("type") == "password"]
        self.assertTrue(passwords)
        for field in passwords:
            self.assertIn(field.get("value"), (None, ""))

    def assert_not_authenticated(self, client=None):
        self.assertNotIn("_auth_user_id", (client or self.client).session)


class RegistrationTests(AccountAssertions, TestCase):
    def register(self, username="StudyUser", follow=False, **changes):
        data = {"username": username, "password1": PUBLIC_PASSWORD, "password2": PUBLIC_PASSWORD}
        data.update(changes)
        return self.client.post(reverse("accounts:register"), data, follow=follow)

    def assert_rejected(self, data, field):
        count = User.objects.count()
        response = self.client.post(reverse("accounts:register"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please correct the errors below.")
        self.assertIn(field, response.context["form"].errors)
        self.assertEqual(User.objects.count(), count)
        self.assert_password_inputs_empty(response)
        self.assert_not_authenticated()
        return response

    def test_registration_fields_and_labels_use_framework_form(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], UserCreationForm)
        page = ParsedPage(response)
        inputs = [field for field in page.inputs if field.get("type") != "hidden"]
        self.assertEqual([field["name"] for field in inputs], ["username", "password1", "password2"])
        for field in inputs:
            self.assertIn(field["id"], page.labels)
            self.assertIn("required", field)
        self.assertContains(response, "No email address is needed.")
        self.assertEqual(User.objects.count(), 0)

    def test_two_independent_users_can_register_and_log_in(self):
        for username in ("StudyUser", "SecondStudent"):
            with self.subTest(username=username):
                response = self.register(username, follow=True)
                self.assertEqual(response.redirect_chain, [(reverse("accounts:login"), 302)])
                self.assert_not_authenticated()
                guidance = response
                self.assertContains(guidance, "Account created. You can now log in.")
                user = User.objects.get(username=username)
                self.assertFalse(user.is_staff)
                self.assertFalse(user.is_superuser)
                self.assertEqual(user.email, "")
                self.assertNotEqual(user.password, PUBLIC_PASSWORD)
                self.assertTrue(user.check_password(PUBLIC_PASSWORD))
                self.assertNotContains(guidance, PUBLIC_PASSWORD)
                login = self.client.post(reverse("accounts:login"), {"username": username, "password": PUBLIC_PASSWORD})
                self.assertRedirects(login, "/")
                self.assertEqual(self.client.session["_auth_user_id"], str(user.pk))
                self.client.post(reverse("accounts:logout"))
        self.assertEqual(User.objects.count(), 2)

    def test_crafted_email_and_privileges_are_ignored(self):
        response = self.register(email="ignored@example.test", is_staff="1", is_superuser="1")
        self.assertRedirects(response, reverse("accounts:login"))
        user = User.objects.get()
        self.assertEqual(user.email, "")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assert_not_authenticated()

    def test_username_trimming_and_nfkc_normalization(self):
        response = self.register("  ＳｔｕｄｙＵｓｅｒ  ")
        self.assertRedirects(response, reverse("accounts:login"))
        self.assertEqual(User.objects.get().username, "StudyUser")

    def test_default_unicode_and_allowed_characters(self):
        username = "Élodie@campus.+-_9"
        self.assertRedirects(self.register(username), reverse("accounts:login"))
        self.assertEqual(User.objects.get().username, username)

    def test_150_character_username_is_accepted(self):
        username = "u" * 150
        self.assertRedirects(self.register(username), reverse("accounts:login"))
        self.assertEqual(User.objects.get().username, username)

    def test_invalid_username_boundaries_create_no_user(self):
        for username in ("u" * 151, "Study User", "Study/User", "", "   "):
            with self.subTest(username=username):
                self.assert_rejected({"username": username, "password1": PUBLIC_PASSWORD, "password2": PUBLIC_PASSWORD}, "username")

    def test_exact_and_ascii_case_duplicate_usernames_are_rejected(self):
        User.objects.create_user(username="StudyUser", password=PUBLIC_PASSWORD)
        for username in ("StudyUser", "studyuser", "STUDYUSER"):
            with self.subTest(username=username):
                response = self.assert_rejected({"username": username, "password1": PUBLIC_PASSWORD, "password2": PUBLIC_PASSWORD}, "username")
                self.assertContains(response, "A user with that username already exists.")
        self.assertEqual(User.objects.get().username, "StudyUser")

    def test_each_missing_registration_field_creates_no_user(self):
        for field in ("username", "password1", "password2"):
            with self.subTest(field=field):
                data = {"username": "StudyUser", "password1": PUBLIC_PASSWORD, "password2": PUBLIC_PASSWORD}
                del data[field]
                self.assert_rejected(data, field)

    def test_password_mismatch_preserves_username_but_not_passwords(self):
        response = self.assert_rejected({"username": "StudyUser", "password1": PUBLIC_PASSWORD, "password2": "Different-Public-Test-Password!294"}, "password2")
        self.assertContains(response, 'value="StudyUser"')
        self.assertNotContains(response, PUBLIC_PASSWORD)
        self.assertNotContains(response, "Different-Public-Test-Password!294")

    def test_all_four_password_validators_reject_invalid_input(self):
        cases = (
            ("SimilarStudent", "SimilarStudent2026", "password_too_similar"),
            ("StudyUser", "S!2", "password_too_short"),
            ("StudyUser", "password", "password_too_common"),
            ("StudyUser", "9236471820", "password_entirely_numeric"),
        )
        for username, password, code in cases:
            with self.subTest(validator=code):
                response = self.assert_rejected({"username": username, "password1": password, "password2": password}, "password2")
                codes = [error.code for error in response.context["form"].errors.as_data()["password2"]]
                self.assertIn(code, codes)

    def test_invalid_username_is_preserved_as_escaped_text(self):
        username = '<script>alert("student")</script>'
        response = self.assert_rejected({"username": username, "password1": PUBLIC_PASSWORD, "password2": PUBLIC_PASSWORD}, "username")
        self.assertContains(response, escape(username))
        self.assertNotContains(response, username)
        self.assertNotContains(response, PUBLIC_PASSWORD)
        field = next(field for field in ParsedPage(response).inputs if field.get("name") == "username")
        self.assertEqual(field["value"], username)


class LoginTests(AccountAssertions, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="StudyUser", password=PUBLIC_PASSWORD)
        User.objects.create_user(username="InactiveStudent", password=PUBLIC_PASSWORD, is_active=False)

    def test_login_fields_have_visible_labels(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        page = ParsedPage(response)
        fields = [field for field in page.inputs if field.get("type") != "hidden"]
        self.assertEqual([field["name"] for field in fields], ["username", "password"])
        for field in fields:
            self.assertIn(field["id"], page.labels)

    def test_valid_stored_spelling_creates_session_and_redirects_home(self):
        response = self.client.post(reverse("accounts:login"), {"username": "StudyUser", "password": PUBLIC_PASSWORD}, follow=True)
        self.assertEqual(response.redirect_chain, [("/", 302)])
        self.assertEqual(self.client.session["_auth_user_id"], str(self.user.pk))
        self.assertContains(response, "You're signed in to StudyTrack.")
        self.assertNotContains(response, PUBLIC_PASSWORD)

    def test_invalid_credentials_case_and_inactive_account_are_generic(self):
        for username, password in (
            ("StudyUser", "Wrong-Public-Test-Password!382"),
            ("MissingStudent", PUBLIC_PASSWORD),
            ("studyuser", PUBLIC_PASSWORD),
            ("InactiveStudent", PUBLIC_PASSWORD),
        ):
            with self.subTest(username=username):
                response = self.client.post(reverse("accounts:login"), {"username": username, "password": password})
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Check your username and password and try again.")
                self.assertContains(response, "Please enter a correct username and password.")
                self.assertContains(response, f'value="{username}"')
                self.assertNotContains(response, password)
                self.assert_password_inputs_empty(response)
                self.assert_not_authenticated()

    def test_missing_login_fields_are_visible_and_do_not_authenticate(self):
        for data in ({}, {"username": "StudyUser"}, {"password": PUBLIC_PASSWORD}):
            with self.subTest(fields=list(data)):
                response = self.client.post(reverse("accounts:login"), data)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Check your username and password and try again.")
                self.assertContains(response, "This field is required.")
                self.assert_password_inputs_empty(response)
                self.assert_not_authenticated()

    def test_invalid_login_username_is_escaped_and_password_not_echoed(self):
        username = '<svg onload="alert(1)">'
        response = self.client.post(reverse("accounts:login"), {"username": username, "password": PUBLIC_PASSWORD})
        self.assertContains(response, escape(username))
        self.assertNotContains(response, username)
        self.assertNotContains(response, PUBLIC_PASSWORD)
        self.assert_password_inputs_empty(response)
        self.assert_not_authenticated()

    def test_local_next_from_get_is_preserved_and_used(self):
        response = self.client.get(reverse("accounts:login"), {"next": "/?welcome=1"})
        self.assertContains(response, 'name="next" value="/?welcome=1"')
        response = self.client.post(reverse("accounts:login"), {"username": "StudyUser", "password": PUBLIC_PASSWORD, "next": "/?welcome=1"})
        self.assertRedirects(response, "/?welcome=1")
        self.assertNotIn(PUBLIC_PASSWORD, response["Location"])

    def test_external_and_untrusted_next_are_ignored(self):
        for destination in ("https://untrusted.example/", "//untrusted.example/", "javascript:alert(1)"):
            with self.subTest(destination=destination):
                client = Client()
                response = client.post(reverse("accounts:login"), {"username": "StudyUser", "password": PUBLIC_PASSWORD, "next": destination})
                self.assertRedirects(response, "/")
                self.assertNotIn(PUBLIC_PASSWORD, response["Location"])


@override_settings(ROOT_URLCONF="tests.account_urls")
class SessionTests(AccountAssertions, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="StudyUser", password=PUBLIC_PASSWORD)

    def login(self):
        response = self.client.post(reverse("accounts:login"), {"username": "StudyUser", "password": PUBLIC_PASSWORD})
        self.assertRedirects(response, "/")

    def test_protected_view_requires_login_and_accepts_authenticated_session(self):
        self.assertRedirects(self.client.get("/__account_test__/"), "/accounts/login/?next=/__account_test__/")
        self.login()
        self.assertContains(self.client.get("/__account_test__/"), "Authenticated access")

    def test_logout_invalidates_session_and_rejects_old_cookie(self):
        self.login()
        old_key = self.client.cookies[settings.SESSION_COOKIE_NAME].value
        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("accounts:login"))
        self.assert_not_authenticated()
        self.assertFalse(Session.objects.filter(session_key=old_key).exists())
        self.assertRedirects(self.client.get("/__account_test__/"), "/accounts/login/?next=/__account_test__/")
        stale_client = Client()
        stale_client.cookies[settings.SESSION_COOKIE_NAME] = old_key
        self.assertRedirects(stale_client.get("/__account_test__/"), "/accounts/login/?next=/__account_test__/")
        home = stale_client.get("/")
        self.assertContains(home, 'href="/accounts/register/"')
        self.assertContains(home, 'href="/accounts/login/"')
        self.assertNotContains(home, 'action="/accounts/logout/"')

    def test_authenticated_get_logout_is_405_without_session_mutation(self):
        self.login()
        old_key = self.client.session.session_key
        response = self.client.get(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(self.client.session.session_key, old_key)
        self.assertEqual(self.client.session["_auth_user_id"], str(self.user.pk))
        self.assertEqual(self.client.get("/__account_test__/").status_code, 200)

    def test_anonymous_logout_access_redirects_to_login(self):
        for method in (self.client.get, self.client.post):
            with self.subTest(method=method.__name__):
                self.assertRedirects(method(reverse("accounts:logout")), "/accounts/login/?next=/accounts/logout/")
                self.assert_not_authenticated()


class PresentationTests(TestCase):
    def test_home_and_account_pages_use_shared_layout_and_styles(self):
        for path, template in (("/", "home.html"), ("/accounts/register/", "accounts/register.html"), ("/accounts/login/", "accounts/login.html")):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, "base.html")
                self.assertTemplateUsed(response, template)
                self.assertContains(response, 'href="/static/css/app.css"')
                self.assertContains(response, 'href="/accounts/register/"')
                self.assertContains(response, 'href="/accounts/login/"')
                self.assertContains(response, "<h1")
                self.assertNotContains(response, 'href="/assignments')

    def test_signed_in_navigation_has_username_and_csrf_logout_on_each_page(self):
        user = User.objects.create_user(username="StudyUser", password=PUBLIC_PASSWORD)
        self.client.force_login(user)
        for path in ("/", "/accounts/register/", "/accounts/login/"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertContains(response, "StudyUser")
                logout = next(form for form in ParsedPage(response).forms if form["attrs"].get("action") == "/accounts/logout/")
                self.assertEqual(logout["attrs"]["method"], "post")
                self.assertTrue(any(field.get("name") == "csrfmiddlewaretoken" and field.get("value") for field in logout["inputs"]))
                self.assertNotContains(response, 'href="/assignments')

    def test_stored_username_is_escaped_in_signed_in_navigation_and_home(self):
        username = '<strong title="student">Unsafe</strong>'
        user = User.objects.create_user(username=username, password=PUBLIC_PASSWORD)
        self.client.force_login(user)
        response = self.client.get("/")
        self.assertContains(response, escape(username))
        self.assertNotContains(response, username)


class CsrfTests(AccountAssertions, TestCase):
    def setUp(self):
        self.csrf_client = Client(enforce_csrf_checks=True)

    def token(self):
        return self.csrf_client.cookies[settings.CSRF_COOKIE_NAME].value

    def test_registration_requires_csrf_and_valid_token_succeeds(self):
        get = self.csrf_client.get(reverse("accounts:register"))
        self.assertContains(get, 'name="csrfmiddlewaretoken"')
        data = {"username": "StudyUser", "password1": PUBLIC_PASSWORD, "password2": PUBLIC_PASSWORD}
        self.assertEqual(self.csrf_client.post(reverse("accounts:register"), data).status_code, 403)
        self.assertEqual(User.objects.count(), 0)
        self.assert_not_authenticated(self.csrf_client)
        response = self.csrf_client.post(reverse("accounts:register"), {**data, "csrfmiddlewaretoken": self.token()})
        self.assertRedirects(response, reverse("accounts:login"))
        self.assertEqual(User.objects.count(), 1)
        self.assert_not_authenticated(self.csrf_client)

    def test_login_requires_csrf_and_valid_token_succeeds(self):
        user = User.objects.create_user(username="StudyUser", password=PUBLIC_PASSWORD)
        get = self.csrf_client.get(reverse("accounts:login"))
        self.assertContains(get, 'name="csrfmiddlewaretoken"')
        data = {"username": "StudyUser", "password": PUBLIC_PASSWORD}
        self.assertEqual(self.csrf_client.post(reverse("accounts:login"), data).status_code, 403)
        self.assert_not_authenticated(self.csrf_client)
        response = self.csrf_client.post(reverse("accounts:login"), {**data, "csrfmiddlewaretoken": self.token()})
        self.assertRedirects(response, "/")
        self.assertEqual(self.csrf_client.session["_auth_user_id"], str(user.pk))

    def test_logout_requires_csrf_and_valid_token_invalidates_session(self):
        user = User.objects.create_user(username="StudyUser", password=PUBLIC_PASSWORD)
        self.csrf_client.force_login(user)
        get = self.csrf_client.get("/")
        self.assertContains(get, 'name="csrfmiddlewaretoken"')
        old_key = self.csrf_client.session.session_key
        self.assertEqual(self.csrf_client.post(reverse("accounts:logout")).status_code, 403)
        self.assertEqual(self.csrf_client.session["_auth_user_id"], str(user.pk))
        self.assertTrue(Session.objects.filter(session_key=old_key).exists())
        response = self.csrf_client.post(reverse("accounts:logout"), {"csrfmiddlewaretoken": self.token()})
        self.assertRedirects(response, reverse("accounts:login"))
        self.assert_not_authenticated(self.csrf_client)
        self.assertFalse(Session.objects.filter(session_key=old_key).exists())
