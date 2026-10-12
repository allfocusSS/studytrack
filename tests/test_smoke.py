from django.test import TestCase


class HomeSmokeTests(TestCase):
    def test_anonymous_root_identifies_studytrack(self):
        with self.assertNumQueries(0):
            response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "StudyTrack")
