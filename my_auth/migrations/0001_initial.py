# Generated by Django 5.1.2 on 2024-11-11 10:09

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('city', '0001_initial'),
        ('team', '0001_initial'),
        ('town_hall', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMobile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=200)),
                ('full_name', models.CharField(max_length=250)),
                ('cpf', models.CharField(max_length=14)),
                ('number_phone', models.CharField(max_length=14)),
                ('password', models.CharField(max_length=250)),
                ('active', models.BooleanField(default=True)),
                ('type', models.CharField(choices=[('Usuário', 'Usuário'), ('Colaborador', 'Colaborador'), ('Coordenador de Equipe', 'Coordenador de Equipe'), ('Administrador', 'Administrador')], default='Usuário', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=250)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('type', models.CharField(choices=[('Usuário', 'Usuário'), ('Colaborador', 'Colaborador'), ('Coordenador de Equipe', 'Coordenador de Equipe'), ('Administrador', 'Administrador')], default='Usuário', max_length=50)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='city_user', to='city.city', verbose_name='Cidade')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_user', to='team.team', verbose_name='Equipe')),
                ('town_hall', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='town_hall_user', to='town_hall.townhall', verbose_name='Prefeitura')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='TokenRecoverPassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=200)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='CodeRecoverPassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='code_recover_user', to='my_auth.usermobile')),
            ],
        ),
    ]