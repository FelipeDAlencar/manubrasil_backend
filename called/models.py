from django.db import models
from problem.models import Problem
from my_auth.models import UserMobile, User
from city.models import City
from service_order.models import ServiceOrder


class Called(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    problem = models.ForeignKey(
        Problem, on_delete=models.SET_NULL, null=True, related_name='called_problem')
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, related_name='city')
    service_order = models.ForeignKey(
        ServiceOrder, on_delete=models.CASCADE, related_name="calleds", verbose_name="Ordem de serviço", null=True, blank=True)

    user_mobile = models.ForeignKey(
        UserMobile, on_delete=models.SET_NULL, null=True, blank=True, related_name='called_user_mobile')
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='called_user')

    localization = models.CharField(max_length=250)
    lat = models.CharField(max_length=100, blank=False, null=False)
    lng = models.CharField(max_length=100, blank=False, null=False)

    status_choice = (
        ("Aberto", 'Aberto'),
        ("Atendido", 'Atendido'),
        ("Não atendido", 'Não atendido'),
    )

    status = models.CharField(
        max_length=15, choices=status_choice, default="Aberto")
    additional_information = models.TextField(null=True, blank=True, default="")
    first_called = models.BooleanField("Primeiro?", default=False)
    class Meta:
        ordering = ['-first_called', '-service_order']


class ImagesCalled(models.Model):
    called = models.ForeignKey(
        Called, on_delete=models.CASCADE, null=False, blank=False, related_name='image_called')
    file = models.FileField(
        upload_to="called_images/", null=False, blank=False)
