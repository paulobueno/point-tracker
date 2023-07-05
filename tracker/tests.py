from django.urls import resolve
from django.test import TestCase
from tracker.views import teams
from django.http import HttpRequest


class HomePageTest(TestCase):

    def test_root_url_resolvers_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, teams)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = teams(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>FooTracker</title>', html)
        self.assertTrue(html.startswith('<!doctype html>'))
        self.assertTrue(html.endswith('</html>'))
