from django.db import models
from city.models import City
class TownHall(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    infos = models.TextField(null=True, blank=True)
    generates_open_os = models.BooleanField(default=False)
    #city = models.ForeignKey(
    #    City, on_delete=models.CASCADE, related_name='town_hall_city', verbose_name="Município")
    
    def __str__(self):
        return self.name + " - " + str(self.id)