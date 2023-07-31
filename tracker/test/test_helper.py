from tracker.models import Point, Pool, Team, Jump


def init_db():
    Point.objects.create_all_points()


def create_team(name='Foo Flyers'):
    return Team.objects.create(name=name)


def create_pool(point_1='A', point_2='J', point_3='15', point_4=None, point_5=None):
    return Pool.objects.create(point_1=Point.objects.filter(name=point_1).first(),
                               point_2=Point.objects.filter(name=point_2).first(),
                               point_3=Point.objects.filter(name=point_3).first(),
                               point_4=Point.objects.filter(name=point_4).first(),
                               point_5=Point.objects.filter(name=point_5).first())


def create_jump(team, pool, date='2020-01-01', points=10):
    return Jump.objects.create(team=team,
                               pool=pool,
                               date=date,
                               points=points)
