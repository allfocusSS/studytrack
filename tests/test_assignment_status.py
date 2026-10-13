from datetime import date, datetime, timezone as datetime_timezone
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from assignments.models import Assignment


class AssignmentStatusTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = get_user_model().objects.create_user('StatusStudent')
        cls.other = get_user_model().objects.create_user('OtherStatusStudent')

    def setUp(self):
        self.client.force_login(self.student)
        self.item = Assignment.objects.create(owner=self.student, title='Private essay', subject='History', description='Private notes', deadline=date(2030, 6, 14))
        self.foreign = Assignment.objects.create(owner=self.other, title='Foreign private title', subject='Foreign private subject', description='Foreign private notes')
        self.url = reverse('assignments:status', args=[self.item.pk])

    def snapshot(self):
        return list(Assignment.objects.order_by('pk').values())

    def test_explicit_transitions_repeat_and_preserve_other_fields(self):
        before = self.snapshot()
        for value, expected, label in [('1', True, 'Completed'), ('1', True, 'Completed'), ('0', False, 'Not completed'), ('0', False, 'Not completed')]:
            with self.subTest(value=value):
                response = self.client.post(self.url, {'is_completed': value, 'owner': self.other.pk, 'title': 'Forged', 'subject': 'Forged', 'description': 'Forged', 'deadline': '2000-01-01', 'created_at': '2000-01-01'}, follow=True)
                self.assertEqual(response.redirect_chain, [('/assignments/', 302)])
                self.assertContains(response, label)
                self.assertContains(self.client.get('/assignments/'), label)
                current = self.snapshot()
                expected_records = [dict(record) for record in before]
                expected_records[0]['is_completed'] = expected
                self.assertEqual(current, expected_records)

    def test_missing_and_invalid_exact_values_leave_all_fields_unchanged(self):
        for data in [{}, *({'is_completed': v} for v in ['', 'true', 'false', '2', ' 1', '01', '-1'])]:
            with self.subTest(data=data):
                before = self.snapshot()
                response = self.client.post(self.url, data)
                self.assertContains(response, 'is_completed must be 1 or 0', status_code=400)
                self.assertEqual(self.snapshot(), before)

    def test_authenticated_get_and_other_methods_cannot_mutate(self):
        for method in ['get', 'head', 'put', 'patch', 'delete', 'options']:
            with self.subTest(method=method):
                before = self.snapshot()
                response = getattr(self.client, method)(self.url)
                self.assertEqual(response.status_code, 405)
                self.assertEqual(self.snapshot(), before)

    def test_anonymous_and_previous_logged_out_session_redirect(self):
        self.client.post('/accounts/logout/')
        for client in [Client(), self.client]:
            for method in ['get', 'post']:
                before = self.snapshot()
                response = client.get(self.url) if method == 'get' else client.post(self.url, {'is_completed': '1'})
                self.assertRedirects(response, '/accounts/login/?next=' + self.url)
                self.assertEqual(self.snapshot(), before)

    def test_valid_foreign_and_missing_requests_return_404_without_disclosure_or_changes(self):
        for pk in [self.foreign.pk, 999999]:
            with self.subTest(pk=pk):
                before = self.snapshot()
                response = self.client.post(reverse('assignments:status', args=[pk]), {'is_completed': '1'})
                self.assertEqual(response.status_code, 404)
                for private in [self.foreign.title, self.foreign.subject, self.foreign.description]:
                    self.assertNotContains(response, private, status_code=404)
                self.assertEqual(self.snapshot(), before)

    def test_enforced_csrf_rejection_and_valid_owned_and_foreign_requests(self):
        self.assertIn('django.middleware.csrf.CsrfViewMiddleware', settings.MIDDLEWARE)
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.student)
        response = client.get('/assignments/')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        before = self.snapshot()
        self.assertEqual(client.post(self.url, {'is_completed': '1'}).status_code, 403)
        self.assertEqual(self.snapshot(), before)
        token = client.cookies['csrftoken'].value
        for pk in [self.foreign.pk, 999999]:
            response = client.post(reverse('assignments:status', args=[pk]), {'is_completed': '1', 'csrfmiddlewaretoken': token})
            self.assertEqual(response.status_code, 404)
            self.assertEqual(self.snapshot(), before)
        self.assertRedirects(client.post(self.url, {'is_completed': '1', 'csrfmiddlewaretoken': token}), '/assignments/')
        self.item.refresh_from_db()
        self.assertTrue(self.item.is_completed)

    def test_rendered_controls_submit_explicit_states_and_empty_list_has_none(self):
        response = self.client.get('/assignments/')
        self.assertContains(response, f'action="{self.url}"')
        self.assertContains(response, 'name="is_completed" value="1"')
        self.assertContains(response, 'Mark completed')
        self.assertNotContains(response, f'href="{self.url}"')
        self.client.post(self.url, {'is_completed': '1'})
        response = self.client.get('/assignments/')
        self.assertContains(response, 'name="is_completed" value="0"')
        self.assertContains(response, 'Mark not completed')
        self.item.delete()
        response = self.client.get('/assignments/')
        self.assertContains(response, 'No assignments yet')
        self.assertNotContains(response, 'class="status-form"')


class AssignmentOverdueTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = get_user_model().objects.create_user('DateStudent')

    def setUp(self):
        self.client.force_login(self.student)

    @patch('django.utils.timezone.now', return_value=datetime(2030, 6, 14, 20, 0, tzinfo=datetime_timezone.utc))
    def test_local_date_boundary_and_all_deadline_status_combinations(self, clock):
        self.assertEqual(settings.TIME_ZONE, 'Asia/Almaty')
        self.assertTrue(settings.USE_TZ)
        with timezone.override('Asia/Almaty'):
            self.client.force_login(self.student)
            self.assertEqual(timezone.localdate(), date(2030, 6, 15))
            self.assertEqual(clock.return_value.date(), date(2030, 6, 14))
            cases = [(False, date(2030, 6, 14), True), (False, date(2030, 6, 15), False), (False, date(2030, 6, 16), False), (False, None, False), (True, date(2030, 6, 14), False), (True, None, False)]
            for completed, deadline, overdue in cases:
                with self.subTest(completed=completed, deadline=deadline):
                    item = Assignment.objects.create(owner=self.student, title='Boundary', subject='Time', deadline=deadline, is_completed=completed)
                    self.assertEqual(item.is_overdue, overdue)
                    response = self.client.get('/assignments/')
                    self.assertContains(response, 'Overdue', count=int(overdue))
                    if deadline is None:
                        self.assertContains(response, 'No deadline')
                    item.delete()

    @patch('django.utils.timezone.localdate', return_value=date(2030, 6, 15))
    def test_completing_removes_overdue_and_reopening_restores_it(self, localdate):
        item = Assignment.objects.create(owner=self.student, title='Past essay', subject='Time', deadline=date(2030, 6, 14))
        url = reverse('assignments:status', args=[item.pk])
        self.assertContains(self.client.get('/assignments/'), 'Overdue')
        response = self.client.post(url, {'is_completed': '1'}, follow=True)
        self.assertContains(response, 'Completed')
        self.assertNotContains(response, 'Overdue')
        self.assertNotContains(self.client.get('/assignments/'), 'Overdue')
        response = self.client.post(url, {'is_completed': '0'}, follow=True)
        self.assertContains(response, 'Not completed')
        self.assertContains(response, 'Overdue')
        self.assertContains(self.client.get('/assignments/'), 'Overdue')
