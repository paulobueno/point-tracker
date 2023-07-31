from django.urls import resolve
from django.test import TestCase

from tracker.models import Point, Pool, Team, Jump
from tracker.test import test_helper
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


class ModelTests(TestCase):

    def test_create_points(self):
        Point.objects.create_all_points()
        randoms = [random for random in 'ABCDEFGHJKLMNOPQ']
        blocks = [str(block) for block in range(1, 23)]
        all_points = randoms + blocks
        for point in Point.objects.all():
            self.assertIn(point.name, all_points)

    def test_point_methods(self):
        randoms = [random for random in 'ABCDEFGHJKLMNOPQ']
        blocks = [str(block) for block in range(1, 23)]
        self.assertEqual(len(Point.objects.get_all_points()), 38)
        self.assertEqual(Point.objects.get_randoms(), randoms)
        self.assertEqual(Point.objects.get_blocks(), blocks)

    def test_create_pool(self):
        Point.objects.create_all_points()
        Pool.objects.create(point_1=Point.objects.filter(name='A').first(),
                            point_2=Point.objects.filter(name='2').first(),
                            point_3=Point.objects.filter(name='14').first())
        self.assertEqual(1, len(Pool.objects.all()))
        self.assertEqual('A', Pool.objects.all().first().point_1.name)
        self.assertEqual('2', Pool.objects.all().first().point_2.name)
        self.assertEqual('14', Pool.objects.all().first().point_3.name)

    def test_create_jump(self):
        test_helper.init_db()
        team = test_helper.create_team()
        pool = test_helper.create_pool()
        Jump.objects.create(team=team,
                            pool=pool,
                            date='2020-01-01',
                            points=10)
        self.assertEqual(Jump.objects.filter(team=team).first().points, 10)
        self.assertEqual(Jump.objects.filter(team=team).first().date.strftime("%Y-%m-%d"), '2020-01-01')


class TestHelpersTest(TestCase):

    def test_init_db(self):
        test_helper.init_db()
        self.assertEqual(len(Point.objects.all()), 38)

    def test_create_team(self):
        test_helper.init_db()
        test_helper.create_team('Test Team')
        self.assertEqual(Team.objects.filter(name='Test Team').first().name, 'Test Team')

    def test_create_pool(self):
        test_helper.init_db()
        test_helper.create_pool('B', 'H', '14')
        stored_pool = Pool.objects.all().first()
        self.assertEqual(stored_pool.point_1.name, 'B')
        self.assertEqual(stored_pool.point_2.name, 'H')
        self.assertEqual(stored_pool.point_3.name, '14')

    def test_create_jump(self):
        test_helper.init_db()
        team = test_helper.create_team()
        pool = test_helper.create_pool()
        test_helper.create_jump(team, pool, '2022-01-01', 15)
        stored_jump = Jump.objects.all().first()
        self.assertEqual(stored_jump.date.strftime("%Y-%m-%d"), '2022-01-01')
        self.assertEqual(stored_jump.points, 15)
