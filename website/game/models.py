from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

#validation checker for unique name
def validate_unique_tag(value):
    players = Player.objects.filter(tag=value)
    if len(players) != 0:
        raise ValidationError('Name already taken', code='duplicate')

#the tile for the game, a row and column location and a value
class Tile(models.Model):
    row = models.IntegerField()
    col = models.IntegerField()
    value = models.IntegerField(default=0)

    @classmethod
    def create_tile(cls, row, col):
        model = cls(row=row, col=col)
        return model

    def __str__(self):
        return f'{self.value}'

#makes a player with a name and gives them a score of 0
class Player(models.Model):
    name = models.CharField(max_length=16, validators=[validate_unique_tag], default='player')
    score = models.IntegerField()

    @classmethod
    def create_player(cls, name):
        model = cls(name=name, score=0)
        return model

    def __str__(self):
        return f'Player {self.name}: {self.score} point(s)'

