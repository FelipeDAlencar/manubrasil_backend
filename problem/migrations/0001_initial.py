# Generated by Django 5.1.2 on 2024-11-11 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('Iluminação', 'Iluminação'), ('Semáforos', 'Semáforos'), ('Buracos', 'Buracos'), ('Bueiros', 'Bueiros'), ('Calçadas', 'Calçadas'), ('Terrenos', 'Terrenos baldios'), ('Outro', 'Outro')], default='Iluminação', max_length=15)),
            ],
        ),
    ]
