from django.db import models
from django.utils import timezone

from django.core.validators import MinValueValidator

from phonenumber_field.modelfields import PhoneNumberField

from .managers import (
    OrderQuerySet,
    ProductQuerySet,
)


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class Order(models.Model):

    class Status(models.TextChoices):
        PROCESSED = 'Обр.', 'Обработан'
        UNPROCESSED = 'Необр.', 'Необработан'

    class PaymentMethod(models.TextChoices):
        CASH = 'Налич.', 'Наличными'
        EMONEY = 'Эл.', 'Электронными'
        UNDEFINED = 'Не указ.', 'Не указано'

    firstname = models.CharField(
        'имя',
        max_length=100
    )
    lastname = models.CharField(
        'фамилия',
        max_length=100
    )
    delivery_address = models.CharField(
        'адрес доставки',
        max_length=100,
        db_index=True
    )
    phonenumber = PhoneNumberField(
        'телефон',
        db_index=True
    )

    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.UNPROCESSED,
        db_index=True,
        verbose_name='статус',
    )

    payment_method = models.CharField(
        max_length=32,
        choices=PaymentMethod.choices,
        default=PaymentMethod.UNDEFINED,
        db_index=True,
        verbose_name='способ оплаты',
    )

    comment = models.CharField(
        'комментарий',
        blank=True,
        max_length=200
    )

    registered_at = models.DateTimeField(
        'дата регистрации',
        default=timezone.now,
        db_index=True
    )

    called_at = models.DateTimeField(
        'дата звонка',
        blank=True,
        null=True,
        db_index=True
    )

    delivered_at = models.DateTimeField(
        'дата доставки',
        blank=True,
        null=True,
        db_index=True
    )

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
        verbose_name='ресторан',
        blank=True
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname} {self.delivery_address}'


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='продукт',
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='заказ'
    )
    quantity = models.SmallIntegerField(
        'кол-во',
        validators=[
            MinValueValidator(limit_value=1, message='значение д.б. больше нуля'),
        ]
    )

    price = models.DecimalField(
        'цена на момент заказа',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказа'

    def __str__(self):
        repr_text = (
            f'Заказ с ID - {self.order.pk}, '
            f'продукт - {self.product.name}'
        )
        return repr_text
