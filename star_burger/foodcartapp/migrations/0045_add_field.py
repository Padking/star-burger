# Generated by Django 3.2 on 2021-12-22 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0044_add_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Налич.', 'Наличными'), ('Эл.', 'Электронными'), ('Не указ.', 'Не указано')], db_index=True, default='Не указ.', max_length=32, verbose_name='способ оплаты'),
        ),
    ]
