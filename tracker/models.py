import uuid
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django_countries.fields import CountryField


class Team(models.Model):
    categories = [
        ('R', 'Rookie'),
        ('I', 'Inter'),
        ('O', 'Open'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=categories, null=True, blank=True)
    foundation = models.DateField(null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    country = CountryField(null=True, blank=True)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    positions = [
        ('P', 'Point'),
        ('T', 'Tail'),
        ('I', 'Inside-Center'),
        ('O', 'Outside-Center')
    ]
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, null=True)
    position = models.CharField(max_length=100, null=True, choices=positions)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    country = CountryField(null=True, blank=True)
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.name) + " (" + str(self.nickname) + ") - " + str(self.team)


class PointManager(models.Manager):
    @staticmethod
    def get_randoms():
        return [random[0] for random in Point.randoms]

    @staticmethod
    def get_blocks():
        return [blocks[0] for blocks in Point.blocks]

    @staticmethod
    def get_all_points():
        return PointManager.get_randoms() + PointManager.get_blocks()

    @staticmethod
    def create_all_points():
        for point in PointManager.get_randoms() + PointManager.get_blocks():
            Point.objects.create(name=point)
        return None


class Point(models.Model):
    randoms = [(random, random) for random in 'ABCDEFGHJKLMNOPQ']
    blocks = [(str(block), str(block)) for block in range(1, 23)]
    name = models.CharField(max_length=2, choices=randoms + blocks, primary_key=True)
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    objects = PointManager()

    def __str__(self):
        return str(self.name)


class Pool(models.Model):
    point_1 = models.ForeignKey(Point, related_name='pool_point_1', on_delete=models.CASCADE, null=True, blank=True)
    point_2 = models.ForeignKey(Point, related_name='pool_point_2', on_delete=models.CASCADE, null=True, blank=True)
    point_3 = models.ForeignKey(Point, related_name='pool_point_3', on_delete=models.CASCADE, null=True, blank=True)
    point_4 = models.ForeignKey(Point, related_name='pool_point_4', on_delete=models.CASCADE, null=True, blank=True)
    point_5 = models.ForeignKey(Point, related_name='pool_point_5', on_delete=models.CASCADE, null=True, blank=True)
    pool_id = models.CharField(max_length=100, primary_key=True, editable=False)
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.pool_id)


@receiver(pre_save, sender=Pool)
def add_pool_id(sender, instance, *args, **kwargs):
    pool = [instance.point_1,
            instance.point_2,
            instance.point_3,
            instance.point_4,
            instance.point_5]
    pool_id = ', '.join([str(point) for point in pool if point is not None])
    instance.pool_id = pool_id


class Jump_Tags(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    label = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.label)


class JumpManager(models.Manager):
    def get_jumps(self, tag=None, team=None, team_category=None, exclude_team=False):
        filters = {'jump_tags__external_id': tag,
                   'team__external_id': team,
                   'team__category': team_category}
        filters = {key: value for key, value in filters.items() if value is not None}
        if exclude_team and team is not None:
            jumps = self.exclude(team__external_id=filters.pop('team__external_id'))
            jumps = jumps.filter(**filters)
        else:
            jumps = self.filter(**filters)
        return jumps


class Jump(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    jump_tags = models.ManyToManyField(Jump_Tags)
    team_members = models.ManyToManyField(TeamMember)
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    video = models.URLField(null=True, blank=True)
    date = models.DateField()
    points = models.IntegerField()
    busts = models.IntegerField(default=0)
    repetition_number = models.IntegerField(editable=False)
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    objects = JumpManager()

    class Meta:
        unique_together = (('team',
                            'pool',
                            'date',
                            'repetition_number'))

    def __str__(self):
        return ' - '.join([str(var) for var in [self.date, self.pool, self.team]]) \
            + " - Jump: " + str(self.repetition_number)


@receiver(pre_save, sender=Jump)
def add_repetition_number(sender, instance, *args, **kwargs):
    jumps = Jump.objects.filter(team=instance.team) \
        .filter(pool=instance.pool) \
        .filter(date=instance.date)
    if not instance.repetition_number:
        instance.repetition_number = len(jumps) + 1


class JumpAnalytic(models.Model):
    jump = models.ForeignKey(Jump, on_delete=models.CASCADE)
    point_number = models.IntegerField()
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    time = models.DecimalField(max_digits=5, decimal_places=2)
    diff = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.BooleanField()
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.jump) + " #" + str(self.point_number)


class Transition(models.Model):
    jump = models.ForeignKey(Jump, on_delete=models.CASCADE)
    point_1 = models.ForeignKey(Point, related_name='transition_point_1', on_delete=models.CASCADE)
    point_2 = models.ForeignKey(Point, related_name='transition_point_2', on_delete=models.CASCADE)
    duration = models.DecimalField(max_digits=5, decimal_places=2)
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.point_1) + ' -> ' + str(self.point_2) + ' - ' + str(self.duration)
