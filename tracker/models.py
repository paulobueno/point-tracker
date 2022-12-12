from django.db import models

randoms = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
    ('F', 'F'),
    ('G', 'G'),
    ('H', 'H'),
    ('J', 'J'),
    ('K', 'K'),
    ('L', 'L'),
    ('M', 'M'),
    ('N', 'N'),
    ('O', 'O'),
    ('P', 'P'),
    ('Q', 'Q')
]
blocks = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('14', '14'),
    ('15', '15'),
    ('16', '16'),
    ('17', '17'),
    ('18', '18'),
    ('19', '19'),
    ('20', '20'),
    ('21', '21')
]


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


class Pool(models.Model):
    point_1 = models.CharField(max_length=10, choices=randoms + blocks, blank=True, null=True)
    point_2 = models.CharField(max_length=10, choices=randoms + blocks, blank=True, null=True)
    point_3 = models.CharField(max_length=10, choices=randoms + blocks, blank=True, null=True)
    point_4 = models.CharField(max_length=10, choices=randoms + blocks, blank=True, null=True)
    point_5 = models.CharField(max_length=10, choices=randoms + blocks, blank=True, null=True)

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


class Transition(models.Model):
    jump = models.ForeignKey(Jump, on_delete=models.CASCADE)
    point_1 = models.CharField(max_length=10, choices=randoms + blocks)
    point_2 = models.CharField(max_length=10, choices=randoms + blocks)
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
