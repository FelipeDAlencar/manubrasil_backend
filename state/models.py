from django.db import models

class State(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    class Meta:
        abstract = False

    def __str__(self):
        return self.name + " - " + str(self.id)