# Generated by Django 5.1.2 on 2024-11-22 11:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('called', '0004_called_date'),
        ('service_order', '0002_alter_serviceorder_calleds'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceorder',
            name='first_called',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fist_called_so', to='called.called', verbose_name='Primeiro chamado'),
        ),
    ]