from django.db import models

class Problem(models.Model):
    description = models.CharField(blank=False, null=False, max_length=200)

    type_choices = (
        ("Iluminação", 'Iluminação'),
        ("Semáforos", 'Semáforos'),
        ("Buracos", 'Buracos'),
        ("Bueiros", 'Bueiros'),
        ("Calçadas", 'Calçadas'),
        ("Terrenos", 'Terrenos baldios'),
        ("Outro", 'Outro'),

    )
    type = models.CharField(
        max_length=15, choices=type_choices, default='Iluminação')