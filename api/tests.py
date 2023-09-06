import json

from django.test import TestCase
from django.urls import resolve, reverse
from api.views import training_points, training_randoms_time
import tracker.test.test_helper as test_helper
from urllib.parse import urlencode


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
        test_helper.create_jump_transitions(jump, [0, 1, 2, 3, 4])

        url = reverse('training_randoms_time', kwargs={'team_external_id': self.team.external_id})
        response = json.loads(self.client.get(url).content.decode('utf-8'))
        self.assertJSONEqual(json.dumps(response[0]), {'date': '2023-01-01',
                                                       'q1': 1,
                                                       'mean': 2,
                                                       'q3': 3})

    def test_training_randoms_time_response_one_jump_pool_only_blocks(self):
        jump = test_helper.create_jump(self.team, self.pool_only_blocks, '2023-01-01')
        test_helper.create_jump_transitions(jump, [10, 2, 30])

        url = reverse('training_randoms_time', kwargs={'team_external_id': self.team.external_id})
        response = json.loads(self.client.get(url).content)
        self.assertJSONEqual(json.dumps(response[0]), {'date': '2023-01-01',
                                                       'q1': 2,
                                                       'mean': 2,
                                                       'q3': 2})

    def test_training_randoms_time_response_two_jumps_pool_mixed_points(self):
        jump_1 = test_helper.create_jump(self.team, self.pool_mixed_points, '2023-01-01')
        jump_2 = test_helper.create_jump(self.team, self.pool_mixed_points, '2023-01-02')
        test_helper.create_jump_transitions(jump_1, [1, 2, 3, 4])
        test_helper.create_jump_transitions(jump_2, [1, 10, 15, 4, 20, 2, 0, 30])

        url = reverse('training_randoms_time', kwargs={'team_external_id': self.team.external_id})
        response = json.loads(self.client.get(url).content)
        self.assertJSONEqual(json.dumps(response[0]), {'date': '2023-01-01',
                                                       'q1': 2.25,
                                                       'mean': 2.5,
                                                       'q3': 2.75})
        self.assertJSONEqual(json.dumps(response[1]), {'date': '2023-01-02',
                                                       'q1': 10,
                                                       'mean': 15,
                                                       'q3': 20})

    def test_filtering_jumps_by_tag(self):
        tag_1 = test_helper.create_jump_tag('tag_1')
        tag_2 = test_helper.create_jump_tag('tag_2')
        jump_1 = test_helper.create_jump(self.team, self.pool_only_randoms, '2023-01-01', 10, [tag_1])
        jump_2 = test_helper.create_jump(self.team, self.pool_only_randoms, '2023-01-02', 10, [tag_2])
        test_helper.create_jump_transitions(jump_1, [0, 1, 2, 3, 4])
        test_helper.create_jump_transitions(jump_2, [0, 1, 2, 3, 4])

        url = (reverse('training_randoms_time', kwargs={'team_external_id': self.team.external_id})
               + '?' + urlencode({'tag_filter': tag_1.external_id}))
        response = json.loads(self.client.get(url).content.decode('utf-8'))
        self.assertEqual(1, len(response))
        self.assertJSONEqual(json.dumps(response[0]), {'date': '2023-01-01',
                                                       'q1': 1,
                                                       'mean': 2,
                                                       'q3': 3})
