from django.db import models


class Location(models.Model):
    address = models.CharField(
        'адрес',
        max_length=100,
        unique=True,
    )

    latitude = models.FloatField(
        'широта',
        blank=True,
        null=True,
    )

    longitude = models.FloatField(
        'долгота',
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        'дата запроса к Я.Геокодеру',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'локация'
        verbose_name_plural = 'локации'

    def __str__(self):
        return self.address
