from django.db import models
from problem.models import Problem
from my_auth.models import UserMobile

class Daily(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    problem  = models.ForeignKey(
        Problem, on_delete=models.SET_NULL, null=True, related_name='daily_problem')
    user  = models.ForeignKey(
        UserMobile, on_delete=models.CASCADE, null=True, related_name='daily_user')

    additional_information=models.TextField(null=True, blank=True)
    city = models.CharField(max_length=200, blank=False, null=False)

class ImagesDaily(models.Model):
    daily = models.ForeignKey(
        Daily, on_delete=models.CASCADE, null=False, blank=False, related_name='image_daily')
    file = models.FileField(
        upload_to="daily_images/", null=False, blank=False)