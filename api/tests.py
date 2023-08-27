import json

from django.test import TestCase
from django.urls import resolve, reverse
from api.views import training_points, training_randoms_time
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
                                                               "avg_points": 25.0}})


class TimeBetweenRandomsTest(TestCase):
    def setUp(self):
        test_helper.init_db()
        self.team = test_helper.create_team()
        self.pool_only_randoms = test_helper.create_pool('A', 'C', 'J')
        self.pool_only_blocks = test_helper.create_pool('1', '14')
        self.pool_mixed_points = test_helper.create_pool('1', 'B', '14')

    def test_url_resolvers_to_endpoint_func(self):
        url = reverse('training_randoms_time', kwargs={'team_external_id': self.team.external_id})
        found = resolve(url)
        self.assertEqual(found.func, training_randoms_time)

    def test_training_randoms_time_response_one_jump_pool_only_randoms(self):
        jump = test_helper.create_jump(self.team, self.pool_only_randoms, '2023-01-01')
        test_helper.create_jump_transitions(jump, [1, 2, 3])

        url = reverse('training_randoms_time', kwargs={'team_external_id': self.team.external_id})
        response = self.client.get(url)
        self.assertJSONEqual(response.content, {'2023-01-01': 2})

    def test_training_randoms_time_response_one_jump_pool_only_blocks(self):
        jump = test_helper.create_jump(self.team, self.pool_only_blocks, '2023-01-01')
        test_helper.create_jump_transitions(jump, [10, 2, 30])

        url = reverse('training_randoms_time', kwargs={'team_external_id': self.team.external_id})
        response = self.client.get(url)
        self.assertJSONEqual(response.content, {'2023-01-01': 2})

    def test_training_randoms_time_response_one_jump_pool_mixed_points(self):
        jump_1 = test_helper.create_jump(self.team, self.pool_mixed_points, '2023-01-01')
        jump_2 = test_helper.create_jump(self.team, self.pool_mixed_points, '2023-01-02')
        test_helper.create_jump_transitions(jump_1, [1, 2, 3, 4])
        test_helper.create_jump_transitions(jump_2, [1, 10, 20, 4])

        url = reverse('training_randoms_time', kwargs={'team_external_id': self.team.external_id})
        response = self.client.get(url)
        self.assertJSONEqual(response.content, {'2023-01-01': 2.5,
                                                '2023-01-02': 15})

