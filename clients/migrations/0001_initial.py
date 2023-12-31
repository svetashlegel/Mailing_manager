# Generated by Django 4.2.4 on 2023-08-18 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150, verbose_name='имя')),
                ('last_name', models.CharField(max_length=150, verbose_name='фамилия')),
                ('nick', models.CharField(max_length=150, unique=True, verbose_name='никнейм')),
                ('email', models.EmailField(max_length=254, verbose_name='почта')),
            ],
        ),
    ]
