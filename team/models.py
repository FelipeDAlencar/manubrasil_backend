from django.db import models
from town_hall.models import TownHall
class Team(models.Model):
    name = models.CharField(max_length=255)
    town_hall = models.ForeignKey(
        TownHall, on_delete=models.CASCADE, null=True, related_name='team_town_hall', verbose_name="Prefeitura")
    
    def __str__(self):
        return self.name + " - " + self.town_hall.name + " - " + str(self.id)
    