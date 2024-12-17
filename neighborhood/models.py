from django.db import models
from city.models import City


class Neighborhood(models.Model):
    name = models.CharField("Nome", max_length=255)
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='neighborhood', verbose_name="Município")

    def __str__(self):
        return self.name + " - " + str(self.id)