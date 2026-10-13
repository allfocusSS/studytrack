from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.html import escape

from assignments.models import Assignment
from tests.test_accounts import PUBLIC_PASSWORD

User = get_user_model()


class AssignmentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create_user("FirstStudent", password=PUBLIC_PASSWORD)
        cls.other = User.objects.create_user("SecondStudent", password=PUBLIC_PASSWORD)

    def setUp(self):
        self.client.force_login(self.student)

    def record(self, **changes):
        values = {"owner": self.student, "title": "Essay", "subject": "History"}
        values.update(changes)
        return Assignment.objects.create(**values)

    def data(self, **changes):
        values = {"title": "Essay", "subject": "History", "description": "", "deadline": ""}
        values.update(changes)
        return values

    def snapshot(self):
        return list(Assignment.objects.order_by("pk").values())

    def test_model_and_empty_list(self):
        response = self.client.get(reverse("assignments:list"))
        self.assertContains(response, "No assignments yet")
        self.assertContains(response, 'href="/assignments/new/"')
        item = self.record()
        self.assertFalse(item.is_completed)
        self.assertEqual(item.description, "")
        self.assertIsNone(item.deadline)
        self.assertIsNotNone(item.created_at)
        self.assertEqual(item.owner, self.student)

    def test_forms_expose_only_editable_fields_and_are_labelled(self):
        item = self.record()
        for url in (reverse("assignments:create"), reverse("assignments:edit", args=[item.pk])):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(list(response.context["form"].fields), ["title", "subject", "description", "deadline"])
                for field in response.context["form"]:
                    self.assertContains(response, f'for="{field.id_for_label}"')
                self.assertContains(response, "Description (optional)")
                self.assertContains(response, "Deadline (optional)")
                self.assertContains(response, 'type="date"')
                self.assertContains(response, "(required)", count=2)

    def test_create_redirect_reload_trim_and_crafted_fields(self):
        response = self.client.post(reverse("assignments:create"), self.data(title="  Essay  ", subject=" History ", owner=self.other.pk, is_completed="1"), follow=True)
        self.assertEqual(response.redirect_chain, [("/assignments/", 302)])
        item = Assignment.objects.get()
        self.assertEqual((item.title, item.subject, item.owner, item.is_completed), ("Essay", "History", self.student, False))
        self.assertContains(response, "Essay")
        self.assertContains(self.client.get("/assignments/"), "No deadline")
        self.assertContains(response, "Not completed")

    def test_optional_values_may_be_omitted_or_empty(self):
        for data in ({"title": "Omitted", "subject": "Math"}, self.data(title="Empty")):
            self.assertRedirects(self.client.post("/assignments/new/", data), "/assignments/")
        self.assertEqual(Assignment.objects.count(), 2)
        for item in Assignment.objects.all():
            self.assertEqual(item.description, "")
            self.assertIsNone(item.deadline)

    def test_exact_lengths_after_trimming_save(self):
        self.assertRedirects(self.client.post("/assignments/new/", self.data(title=" " + "T" * 160 + " ", subject=" " + "S" * 100 + " ", description="D" * 5000)), "/assignments/")
        item = Assignment.objects.get()
        self.assertEqual((len(item.title), len(item.subject), len(item.description)), (160, 100, 5000))

    def test_required_empty_whitespace_and_omitted_fields_reject_create_and_edit(self):
        item = self.record(description="Stored", deadline=date(2030, 1, 2))
        for field in ("title", "subject"):
            for value in (None, "", " \t "):
                data = self.data()
                if value is None:
                    del data[field]
                else:
                    data[field] = value
                for url in ("/assignments/new/", reverse("assignments:edit", args=[item.pk])):
                    with self.subTest(field=field, value=value, url=url):
                        before = self.snapshot()
                        response = self.client.post(url, data)
                        self.assertEqual(response.status_code, 200)
                        self.assertIn(field, response.context["form"].errors)
                        self.assertContains(response, "This field is required.")
                        self.assertEqual(self.snapshot(), before)

    def test_over_length_fields_reject_create_and_edit(self):
        item = self.record()
        for field, value in (("title", "T" * 161), ("subject", "S" * 101), ("description", "D" * 5001)):
            for url in ("/assignments/new/", reverse("assignments:edit", args=[item.pk])):
                with self.subTest(field=field, url=url):
                    before = self.snapshot()
                    response = self.client.post(url, self.data(**{field: value}))
                    self.assertIn(field, response.context["form"].errors)
                    self.assertContains(response, "Ensure this value has at most")
                    self.assertEqual(self.snapshot(), before)

    def test_past_today_future_dates_save(self):
        # Fixed reference dates make this deterministic; acceptance does not reject past dates.
        today = date(2026, 10, 13)
        for day in (today - timedelta(days=1), today, today + timedelta(days=1)):
            self.assertRedirects(self.client.post("/assignments/new/", self.data(deadline=day.isoformat())), "/assignments/")
            self.assertTrue(Assignment.objects.filter(deadline=day).exists())

    def test_malformed_and_impossible_dates_do_not_mutate(self):
        item = self.record(deadline=date(2030, 1, 2))
        for value in ("not-a-date", "2026-02-30", "2026-13-01", "13/10/2026"):
            for url in ("/assignments/new/", reverse("assignments:edit", args=[item.pk])):
                with self.subTest(value=value, url=url):
                    before = self.snapshot()
                    response = self.client.post(url, self.data(deadline=value))
                    self.assertIn("deadline", response.context["form"].errors)
                    self.assertContains(response, "Enter a valid date.")
                    self.assertContains(response, f'value="{value}"')
                    self.assertEqual(self.snapshot(), before)

    def test_private_list_displays_fields_status_and_owned_controls(self):
        owned = self.record(description="Private notes", deadline=date(2030, 1, 2), is_completed=True)
        foreign = self.record(owner=self.other, title="Foreign title", subject="Foreign subject", description="Foreign description")
        response = self.client.get("/assignments/")
        self.assertEqual(list(response.context["assignments"]), [owned])
        for text in ("Essay", "History", "Private notes", "2 Jan 2030", "Completed"):
            self.assertContains(response, text)
        for text in (foreign.title, foreign.subject, foreign.description):
            self.assertNotContains(response, text)
        for name in ("edit", "delete"):
            self.assertContains(response, f'href="{reverse("assignments:" + name, args=[owned.pk])}"')
        self.client.force_login(self.other)
        self.assertEqual(list(self.client.get("/assignments/").context["assignments"]), [foreign])

    def test_edit_prefilled_and_only_selected_record_changes(self):
        item = self.record(description="Original", deadline=date(2030, 1, 2), is_completed=True)
        second = self.record(title="Keep this")
        before_second = Assignment.objects.filter(pk=second.pk).values().get()
        url = reverse("assignments:edit", args=[item.pk])
        response = self.client.get(url)
        self.assertContains(response, 'value="Essay"')
        self.assertContains(response, "Original")
        self.assertContains(response, 'value="2030-01-02"')
        response = self.client.post(url, self.data(title=" Revised ", subject=" Science ", description="New notes", deadline="2031-02-03", owner=self.other.pk, is_completed="0"), follow=True)
        self.assertEqual(response.redirect_chain, [("/assignments/", 302)])
        item.refresh_from_db()
        self.assertEqual((item.title, item.subject, item.description, item.deadline), ("Revised", "Science", "New notes", date(2031, 2, 3)))
        self.assertEqual(item.owner, self.student)
        self.assertTrue(item.is_completed)
        self.assertEqual(Assignment.objects.filter(pk=second.pk).values().get(), before_second)
        self.assertContains(self.client.get("/assignments/"), "New notes")

    def test_add_change_clear_deadline_and_description(self):
        item = self.record(is_completed=True)
        for description, deadline in (("Added", "2030-01-02"), ("Changed", "2031-02-03"), ("", "")):
            self.assertRedirects(self.client.post(reverse("assignments:edit", args=[item.pk]), self.data(description=description, deadline=deadline)), "/assignments/")
            item.refresh_from_db()
            self.assertEqual(item.description, description)
            self.assertEqual(item.deadline, date.fromisoformat(deadline) if deadline else None)
            self.assertTrue(item.is_completed)
            self.assertEqual(item.owner, self.student)

    def test_failed_forms_preserve_other_fields_and_all_stored_values(self):
        item = self.record(description="Stored", deadline=date(2030, 1, 2), is_completed=True)
        for url in ("/assignments/new/", reverse("assignments:edit", args=[item.pk])):
            before = self.snapshot()
            response = self.client.post(url, self.data(title="", subject="Biology", description="Keep these notes", deadline="2032-03-04"))
            self.assertContains(response, "Check your details")
            self.assertContains(response, 'value="Biology"')
            self.assertContains(response, "Keep these notes")
            self.assertContains(response, 'value="2032-03-04"')
            self.assertEqual(self.snapshot(), before)

    def test_get_pages_and_delete_cancel_never_mutate(self):
        item = self.record()
        before = self.snapshot()
        for url in ("/assignments/", "/assignments/new/", reverse("assignments:edit", args=[item.pk]), reverse("assignments:delete", args=[item.pk])):
            self.assertEqual(self.client.get(url).status_code, 200)
            self.assertEqual(self.snapshot(), before)
        confirmation = self.client.get(reverse("assignments:delete", args=[item.pk]))
        self.assertContains(confirmation, "Essay")
        self.assertContains(confirmation, 'href="/assignments/">Cancel</a>')
        self.assertContains(confirmation, '>Delete</button>')
        self.client.get("/assignments/")
        self.assertEqual(self.snapshot(), before)

    def test_delete_selected_only_and_deleted_id_is_404(self):
        selected = self.record()
        keep = self.record(title="Keep")
        foreign = self.record(owner=self.other, title="Foreign")
        before = list(Assignment.objects.exclude(pk=selected.pk).order_by("pk").values())
        self.assertRedirects(self.client.post(reverse("assignments:delete", args=[selected.pk])), "/assignments/")
        self.assertFalse(Assignment.objects.filter(pk=selected.pk).exists())
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.client.get(reverse("assignments:edit", args=[selected.pk])).status_code, 404)
        self.assertEqual(self.client.get(reverse("assignments:delete", args=[selected.pk])).status_code, 404)

    def test_foreign_and_missing_ids_404_no_disclosure_or_changes(self):
        foreign = self.record(owner=self.other, title="Hidden foreign title", subject="Hidden subject", description="Hidden notes")
        self.record()
        before = self.snapshot()
        for pk in (foreign.pk, foreign.pk + 999):
            for name in ("edit", "delete"):
                for method in (self.client.get, self.client.post):
                    with self.subTest(pk=pk, name=name, method=method.__name__):
                        response = method(reverse("assignments:" + name, args=[pk]), self.data(title="Attacker", owner=self.student.pk))
                        self.assertEqual(response.status_code, 404)
                        for text in (foreign.title, foreign.subject, foreign.description):
                            self.assertNotContains(response, text, status_code=404)
                        self.assertEqual(self.snapshot(), before)

    def test_anonymous_and_logged_out_routes_deny_access_without_mutation(self):
        item = self.record()
        old_cookie = self.client.cookies[settings.SESSION_COOKIE_NAME].value
        self.client.post("/accounts/logout/")
        stale = Client()
        stale.cookies[settings.SESSION_COOKIE_NAME] = old_cookie
        before = self.snapshot()
        for client in (Client(), self.client, stale):
            for url in ("/assignments/", "/assignments/new/", reverse("assignments:edit", args=[item.pk]), reverse("assignments:delete", args=[item.pk])):
                for method in (client.get, client.post):
                    response = method(url) if method.__name__ == "get" else method(url, self.data(title="Attack"))
                    self.assertRedirects(response, "/accounts/login/?next=" + url)
                    self.assertEqual(self.snapshot(), before)

    def test_user_text_escaped_in_list_forms_errors_and_confirmation(self):
        title = '<script>alert("title")</script>'
        subject = '<svg onload="alert(1)">'
        description = '</textarea><img src=x onerror="alert(1)">'
        item = self.record(title=title, subject=subject, description=description)
        for url in ("/assignments/", reverse("assignments:edit", args=[item.pk]), reverse("assignments:delete", args=[item.pk])):
            response = self.client.get(url)
            for text in (title, subject):
                self.assertContains(response, escape(text))
                self.assertNotContains(response, text)
            if "delete" not in url:
                self.assertContains(response, escape(description))
                self.assertNotContains(response, description)
        for url in ("/assignments/new/", reverse("assignments:edit", args=[item.pk])):
            response = self.client.post(url, self.data(title=title, subject=subject, description=description, deadline="invalid"))
            for text in (title, subject, description):
                self.assertContains(response, escape(text))
                self.assertNotContains(response, text)

    def test_shared_layout_existing_navigation_and_account_contract(self):
        item = self.record()
        for url in ("/", "/accounts/login/", "/accounts/register/", "/assignments/", "/assignments/new/", reverse("assignments:edit", args=[item.pk]), reverse("assignments:delete", args=[item.pk])):
            response = self.client.get(url)
            self.assertTemplateUsed(response, "base.html")
            self.assertContains(response, 'href="/static/css/app.css"')
            self.assertContains(response, 'href="/assignments/"')
            self.assertContains(response, 'href="/assignments/new/"')
            self.assertContains(response, "FirstStudent")
            self.assertContains(response, 'action="/accounts/logout/"')

    def test_list_post_is_rejected_without_mutation(self):
        self.record()
        before = self.snapshot()
        self.assertEqual(self.client.post("/assignments/", self.data()).status_code, 405)
        self.assertEqual(self.snapshot(), before)

    def test_unsupported_mutating_methods_are_405_without_mutation(self):
        item = self.record()
        before = self.snapshot()
        for url in ("/assignments/", "/assignments/new/", reverse("assignments:edit", args=[item.pk]), reverse("assignments:delete", args=[item.pk])):
            for method in (self.client.put, self.client.patch, self.client.delete):
                with self.subTest(url=url, method=method.__name__):
                    self.assertEqual(method(url, self.data(title="Attack")).status_code, 405)
                    self.assertEqual(self.snapshot(), before)

    def test_enforced_csrf_create_edit_delete_forms_and_mutations(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.student)
        item = self.record()
        for url in ("/assignments/new/", reverse("assignments:edit", args=[item.pk]), reverse("assignments:delete", args=[item.pk])):
            with self.subTest(url=url):
                get = client.get(url)
                self.assertContains(get, 'name="csrfmiddlewaretoken"')
                before = self.snapshot()
                self.assertEqual(client.post(url, self.data(title="CSRF protected")).status_code, 403)
                self.assertEqual(self.snapshot(), before)
                token = client.cookies[settings.CSRF_COOKIE_NAME].value
                response = client.post(url, self.data(title="CSRF protected", csrfmiddlewaretoken=token))
                self.assertRedirects(response, "/assignments/")
                if "new" in url:
                    self.assertEqual(Assignment.objects.count(), len(before) + 1)
                elif "edit" in url:
                    item.refresh_from_db()
                    self.assertEqual(item.title, "CSRF protected")
                else:
                    self.assertFalse(Assignment.objects.filter(pk=item.pk).exists())
