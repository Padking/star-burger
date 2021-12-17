from rest_framework import serializers
from rest_framework.fields import ListField

from .models import (
    Order,
    Product,
)


class ProductSerializer(serializers.Serializer):
    product = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1)

    def validate_product(self, value):
        product_exist = Product.objects.filter(id=value).exists()
        if not product_exist:
            raise serializers.ValidationError(
                'invalid identifier of "product" in "products" key'
            )

        return value


class OrderSerializer(serializers.ModelSerializer):
    address = serializers.CharField(source='delivery_address')

    products = ListField(child=ProductSerializer(), allow_empty=False,
                         write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname', 'phonenumber', 'address', 'products', ]
