# Generated by Django 5.1.2 on 2024-12-12 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('called', '0011_alter_called_additional_information'),
    ]

    operations = [
        migrations.AlterField(
            model_name='called',
            name='first_called',
            field=models.BooleanField(default=False, verbose_name='Primeiro?'),
        ),
    ]