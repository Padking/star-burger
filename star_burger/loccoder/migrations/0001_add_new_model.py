# Generated by Django 3.2 on 2021-12-28 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100, unique=True, verbose_name='адрес')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='широта')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='долгота')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='дата запроса к Я.Геокодеру')),
            ],
            options={
                'verbose_name': 'локация',
                'verbose_name_plural': 'локации',
            },
        ),
    ]
