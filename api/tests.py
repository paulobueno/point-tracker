import json

from django.test import TestCase
from django.urls import resolve, reverse
from api.views import training_points
import tracker.test.test_helper as test_helper


class TrainingPointsApiTest(TestCase):

    def setUp(self):
        test_helper.init_db()
        self.team = test_helper.create_team()
        self.pool = test_helper.create_pool('A', '14', 'F')

    def test_url_resolvers_to_endpoint_func(self):
        url = reverse('training_points', kwargs={'team_external_id': self.team.external_id})
        found = resolve(url)
        self.assertEqual(found.func, training_points)

    def test_training_points_response(self):
        test_helper.create_jump(self.team, self.pool, '2020-01-01', 10)
        test_helper.create_jump(self.team, self.pool, '2020-01-01', 20)
        test_helper.create_jump(self.team, self.pool, '2020-01-02', 5)
        test_helper.create_jump(self.team, self.pool, '2020-01-02', 45)
        test_helper.create_jump(self.team, self.pool, '2020-01-02', 25)
        url = reverse('training_points', kwargs={'team_external_id': self.team.external_id})
        response = self.client.get(url)
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(sorted(response_content.keys()), ['2020-01-01', '2020-01-02'])
        self.assertJSONEqual(response.content, {"2020-01-01": {"total_jumps": 2,
                                                               "avg_points": 15.0},
                                                "2020-01-02": {"total_jumps": 3,
                                                               "avg_points": 25.0}
                                                })
