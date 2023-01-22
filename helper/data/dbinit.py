# import django
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'point_tracker.settings')
# django.setup()

from tracker.models import Team, Point

randoms = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'),
           ('F', 'F'), ('G', 'G'), ('H', 'H'), ('J', 'J'), ('K', 'K'),
           ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q')]
blocks = [(str(block), str(block)) for block in range(1, 23)]


def main():
    teams = ['FooFlyers', 'INIT-Y', 'Mineours', 'Netunos']
    for team in teams:
        Team(name=team, foundation='2020-01-01').save()
    for (point, _) in randoms + blocks:
        Point(name=point).save()


if __name__ == '__main__':
    main()
