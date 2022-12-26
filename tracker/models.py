from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)
    foundation = models.DateField()

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
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.name) + " (" + str(self.nickname) + ") - " + str(self.team)


class Point(models.Model):
    randoms = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'),
               ('F', 'F'), ('G', 'G'), ('H', 'H'), ('J', 'J'), ('K', 'K'),
               ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q')]
    blocks = [(str(block), str(block)) for block in range(1, 23)]
    name = models.CharField(max_length=2, choices=randoms + blocks, primary_key=True)

    def __str__(self):
        return str(self.name)


class Pool(models.Model):
    point_1 = models.ForeignKey(Point, related_name='pool_point_1', on_delete=models.CASCADE, null=True, blank=True)
    point_2 = models.ForeignKey(Point, related_name='pool_point_2', on_delete=models.CASCADE, null=True, blank=True)
    point_3 = models.ForeignKey(Point, related_name='pool_point_3', on_delete=models.CASCADE, null=True, blank=True)
    point_4 = models.ForeignKey(Point, related_name='pool_point_4', on_delete=models.CASCADE, null=True, blank=True)
    point_5 = models.ForeignKey(Point, related_name='pool_point_5', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return ', '.join([str(var) for var in
                          [self.point_1, self.point_2, self.point_3, self.point_4, self.point_5]
                          if var is not None])


class Jump(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    video = models.URLField(null=True, blank=True)
    date = models.DateField()
    points = models.IntegerField()
    busts = models.IntegerField(default=0)

    def __str__(self):
        return ' - '.join([str(var) for var in [self.date, self.pool, self.team]])


class JumpAnalytic(models.Model):
    jump = models.ForeignKey(Jump, on_delete=models.CASCADE)
    point_number = models.IntegerField()
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    time = models.DecimalField(max_digits=2, decimal_places=1)
    diff = models.DecimalField(max_digits=2, decimal_places=1)
    status = models.BooleanField()

    def __str__(self):
        return self.jump


class Transition(models.Model):
    jump = models.ForeignKey(Jump, on_delete=models.CASCADE)
    point_1 = models.ForeignKey(Point, related_name='transition_point_1', on_delete=models.CASCADE, null=True)
    point_2 = models.ForeignKey(Point, related_name='transition_point_2', on_delete=models.CASCADE, null=True)
    duration_1 = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)
    duration_2 = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)
    duration_3 = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)
    duration_4 = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)
    duration_5 = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)
    duration_6 = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)
    duration_7 = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)
    duration_8 = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)
    duration_9 = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)
    duration_10 = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)

    def __str__(self):
        return str(self.point_1) + ' -> ' + str(self.point_2) + ' : ' + str(self.jump)
