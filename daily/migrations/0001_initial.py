# Generated by Django 5.1.2 on 2024-11-12 10:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('my_auth', '0001_initial'),
        ('problem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Daily',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('additional_information', models.TextField(blank=True, null=True)),
                ('city', models.CharField(max_length=200)),
                ('problem', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='daily_problem', to='problem.problem')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='daily_user', to='my_auth.usermobile')),
            ],
        ),
        migrations.CreateModel(
            name='ImagesCalled',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='daily_images/')),
                ('daily', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_daily', to='daily.daily')),
            ],
        ),
    ]