# Generated by Django 3.2 on 2021-12-17 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0039_rename_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Обр.', 'Обработан'), ('Необр.', 'Необработан')], db_index=True, default='Необр.', max_length=32, verbose_name='статус'),
        ),
    ]
