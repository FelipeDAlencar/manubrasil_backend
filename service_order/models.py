from django.db import models


class ServiceOrder(models.Model):
    status_choice = (
        ("Requisitada", 'Requisitada'),
        ("Rejeitada", 'Rejeitada'),
        ("Aberta", 'Aberta'),
        ("Concluída", 'Concluída'),
    )

    status = models.CharField(
        max_length=15, choices=status_choice, default="Requisitada")
    create_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True, default="")
    open_date = models.DateTimeField(null=True, blank=True)
    
