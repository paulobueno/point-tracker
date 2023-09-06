from tracker.models import Point, Pool, Team, Jump, Transition, Jump_Tags
from itertools import cycle, islice, pairwise


def init_db():
    Point.objects.create_all_points()


def create_team(name='Foo Flyers'):
    return Team.objects.create(name=name)


def create_pool(point_1, point_2, point_3=None, point_4=None, point_5=None):
    return Pool.objects.create(point_1=Point.objects.filter(name=point_1).first(),
                               point_2=Point.objects.filter(name=point_2).first(),
                               point_3=Point.objects.filter(name=point_3).first(),
                               point_4=Point.objects.filter(name=point_4).first(),
                               point_5=Point.objects.filter(name=point_5).first())


def create_jump(team, pool, date='2020-01-01', points=10, jump_tags=None):
    jump = Jump.objects.create(team=team,
                               pool=pool,
                               date=date,
                               points=points)
    if isinstance(jump_tags, list) and len(jump_tags) > 0:
        jump.jump_tags.set(jump_tags)
    return jump


def create_jump_transition(jump, duration=2, point_1='A', point_2='B'):
    return Transition.objects.create(jump=jump,
                                     point_1=point_1,
                                     point_2=point_2,
                                     duration=duration)


def get_point(point):
    return Point.objects.get(name=point)


def create_jump_transitions(jump, durations):
    pool_points = [jump.pool.point_1,
                   jump.pool.point_2,
                   jump.pool.point_3,
                   jump.pool.point_4,
                   jump.pool.point_5]
    final_pool_points = []
    for point in [point for point in pool_points if point is not None]:
        if point.name in Point.objects.get_blocks():
            final_pool_points.append(point)
            final_pool_points.append(point)
        else:
            final_pool_points.append(point)
    pool = pairwise(cycle(final_pool_points))

    for duration in durations:
        points = next(pool)
        create_jump_transition(jump, duration, points[0], points[1])


def create_jump_tag(label):
    return Jump_Tags.objects.create(label=label)
