from django.db import models
from state.models import State


class City(models.Model):
    name = models.CharField(max_length=255,)
    latitude = models.CharField("Latitude", max_length=150)
    longitude = models.CharField("Longitude", max_length=150)
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, null=True, related_name='city_state', verbose_name="Estado")

    def __str__(self):
        return self.name + " - " + str(self.id)
