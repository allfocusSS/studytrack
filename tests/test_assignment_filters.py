from datetime import date, datetime, timezone

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.utils.html import escape

from assignments.models import Assignment


class AssignmentFilterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = get_user_model().objects.create_user('FilterStudent')
        cls.other = get_user_model().objects.create_user('ForeignFilterStudent')

    def setUp(self):
        self.client.force_login(self.student)
        self.pending = self.record('Pending Physics', 'Physics')
        self.completed = self.record('Completed Physics', 'Physics', is_completed=True)
        self.lowercase = self.record('Lower physics', 'physics')
        self.foreign = self.record('Private foreign assignment title', 'Foreign confidential subject', owner=self.other)

    def record(self, title, subject, **changes):
        return Assignment.objects.create(owner=changes.pop('owner', self.student), title=title, subject=subject, **changes)

    def snapshot(self):
        return list(Assignment.objects.order_by('pk').values())

    def request(self, parameters, expected, status=200):
        before = self.snapshot()
        response = self.client.get('/assignments/', parameters)
        self.assertEqual(response.status_code, status)
        self.assertEqual(self.snapshot(), before)
        self.assertNotContains(response, self.foreign.title, status_code=status)
        self.assertNotContains(response, self.foreign.subject, status_code=status)
        if status == 200:
            self.assertEqual([x.pk for x in response.context['assignments']], [x.pk for x in expected])
        return response

    def test_all_absent_empty_and_explicit_status(self):
        for value in [None, '', 'all', 'pending', 'completed']:
            with self.subTest(value=value):
                expected = [self.pending, self.completed, self.lowercase]
                if value == 'pending': expected = [self.pending, self.lowercase]
                if value == 'completed': expected = [self.completed]
                response = self.request({} if value is None else {'status': value}, expected)
                self.assertContains(response, f'value="{value or "all"}" selected')

    def test_invalid_status_readable_safe_and_unchanged(self):
        for value in ['unknown', 'true', 'Pending', ' all', '<script>alert(1)</script>']:
            with self.subTest(value=value):
                response = self.request({'status': value}, [], status=400)
                self.assertContains(response, 'Choose a valid status', status_code=400)
                self.assertNotContains(response, '<script>', status_code=400)

    def test_distinct_owned_options_unaffected_by_filter(self):
        for parameters in [{}, {'status': 'completed'}, {'subject': 'unknown'}, {'status': 'pending', 'subject': 'Physics'}]:
            response = self.client.get('/assignments/', parameters)
            self.assertEqual(response.context['subjects'], ['Physics', 'physics'])
            self.assertContains(response, '<option value="">All subjects</option>')
            self.assertContains(response, '<option value="Physics"', count=1)
            self.assertContains(response, '<option value="physics"', count=1)
            self.assertNotContains(response, '<option value="unknown"')
            self.assertNotContains(response, self.foreign.subject)

    def test_exact_case_subject_and_empty_absent_unknown_foreign_only(self):
        for value, expected in [(None, [self.pending, self.completed, self.lowercase]), ('', [self.pending, self.completed, self.lowercase]), ('Physics', [self.pending, self.completed]), ('physics', [self.lowercase]), (' Physics', []), ('Physics ', []), ('PHYSICS', []), ('Unknown', [])]:
            with self.subTest(value=value):
                self.request({} if value is None else {'subject': value}, expected)
        before = self.snapshot()
        response = self.client.get('/assignments/', {'subject': self.foreign.subject})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['assignments']), [])
        self.assertEqual(response.context['subjects'], ['Physics', 'physics'])
        self.assertNotContains(response, self.foreign.title)
        self.assertNotContains(response, f'<option value="{self.foreign.subject}"')
        self.assertEqual(self.snapshot(), before)

    def test_and_selected_values_no_matches_clear_and_unknown_escaped(self):
        response = self.request({'subject': 'Physics', 'status': 'completed'}, [self.completed])
        self.assertContains(response, 'value="completed" selected')
        self.assertContains(response, 'value="Physics" selected')
        response = self.request({'subject': 'physics', 'status': 'completed'}, [])
        self.assertContains(response, 'No assignments match your filters')
        self.assertContains(response, 'href="/assignments/">Clear filters')
        value = '<script>' + 'Z' * 100 + '</script>'
        response = self.request({'subject': value}, [])
        self.assertContains(response, 'Active subject: ' + escape(value))
        self.assertNotContains(response, '<script>')
        self.assertNotContains(response, '<option value="' + escape(value))
        self.request({}, [self.pending, self.completed, self.lowercase])

    def test_empty_account_filters_and_anonymous_redirect(self):
        Assignment.objects.filter(owner=self.student).delete()
        response = self.request({}, [])
        self.assertContains(response, 'No assignments yet')
        self.assertContains(response, 'Add assignment')
        self.assertEqual(response.context['subjects'], [])
        for value in ['all', 'pending', 'completed']:
            self.assertContains(response, f'<option value="{value}"')
        self.assertContains(response, 'method="get" action="/assignments/"')
        self.assertRedirects(Client().get('/assignments/'), '/accounts/login/?next=/assignments/')

    def test_dated_null_deadline_created_and_pk_ties_in_all_filters(self):
        Assignment.objects.filter(owner=self.student).delete()
        early = datetime(2030, 1, 1, tzinfo=timezone.utc)
        late = datetime(2030, 1, 2, tzinfo=timezone.utc)
        # Insert in a deliberately different order from dates and timestamps.
        null_late = self.record('Null late', 'Order', is_completed=True)
        later_date = self.record('Later date', 'Order', deadline=date(2030, 6, 2))
        tie_first = self.record('Date tie first', 'Order', deadline=date(2030, 6, 1), is_completed=True)
        tie_second = self.record('Date tie second', 'Order', deadline=date(2030, 6, 1), is_completed=True)
        date_late_created = self.record('Date late created', 'Order', deadline=date(2030, 6, 1))
        null_first = self.record('Null tie first', 'Order', is_completed=True)
        null_second = self.record('Null tie second', 'Order')
        for item in [later_date, tie_first, tie_second, null_first, null_second]:
            Assignment.objects.filter(pk=item.pk).update(created_at=early)
        for item in [null_late, date_late_created]:
            Assignment.objects.filter(pk=item.pk).update(created_at=late)
        expected = [tie_first, tie_second, date_late_created, later_date, null_first, null_second, null_late]
        for parameters, result in [({}, expected), ({'subject': 'Order'}, expected), ({'status': 'completed'}, [tie_first, tie_second, null_first, null_late]), ({'subject': 'Order', 'status': 'pending'}, [date_late_created, later_date, null_second])]:
            with self.subTest(parameters=parameters):
                self.request(parameters, result)
