from typing import (
    Dict,
    List
)

import phonenumbers

from rest_framework import serializers
from rest_framework import status

from .models import Product


def validate_products_key(products: List[Dict]):

    detail = ''
    if isinstance(products, str) or not products:
        detail = {'error': '"products" key not presented or not filled out list'}
    else:
        for product in products:
            product_id = product['product']
            product_exist = Product.objects.filter(id=product_id).exists()
            if not product_exist:
                detail = {'error': 'invalid identifier of "product" in "products" key'}

    if detail:
        raise serializers.ValidationError(detail, code=status.HTTP_400_BAD_REQUEST)


def validate_keys_combinations(keys_values_combinations: List):
    if not all(keys_values_combinations):
        detail = {'error': (
            'one or more values from keys: "firstname", "lastname", '
            '"phonenumber", "address" not presented or not str'
        )}  # FIXME

        raise serializers.ValidationError(detail, code=status.HTTP_400_BAD_REQUEST)


def validate_phonenumber_key(raw_phone_number: str, region='RU'):
    try:
        phone_number = phonenumbers.parse(raw_phone_number, region=region)
    except phonenumbers.NumberParseException:
        phone_number = phonenumbers.phonenumber.PhoneNumber()

    possible_number = phonenumbers.is_possible_number(phone_number)
    valid_number = phonenumbers.is_valid_number(phone_number)

    normalized = possible_number and valid_number

    if not normalized:
        detail = {'error': '"phonenumber" key not presented or not normalized'}
        raise serializers.ValidationError(detail, code=status.HTTP_400_BAD_REQUEST)


def validate_order_fields(order: Dict):

    products = order.get('products', None)
    validate_products_key(products)

    phonenumber = order.get('phonenumber', None)
    validate_phonenumber_key(phonenumber)

    order_form_keys = [
        order.get('firstname', None),
        order.get('lastname', None),
        order.get('phonenumber', None),
        order.get('address', None),
    ]
    validate_keys_combinations(order_form_keys)
