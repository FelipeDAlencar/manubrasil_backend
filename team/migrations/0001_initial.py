# Generated by Django 5.1.2 on 2024-11-08 12:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('town_hall', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('town_hall', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_town_hall', to='town_hall.townhall', verbose_name='Prefeitura')),
            ],
        ),
    ]
