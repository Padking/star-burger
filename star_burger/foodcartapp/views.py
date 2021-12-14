from django.http import JsonResponse
from django.templatetags.static import static

from rest_framework.decorators import api_view

from .models import (
    Order,
    OrderItem,
    Product,
)


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    try:
        about_order = request.data
    except Exception:  # FIXME
        raise
    else:
        order = Order.objects.create(firstname=about_order['firstname'],
                                     lastname=about_order['lastname'],
                                     phonenumber=about_order['phonenumber'],
                                     delivery_address=about_order['address'])
        products = about_order['products']
        for product in products:
            product_id = product['product']
            prod = Product.objects.get(id=product_id)  # FIXME
            quantity = product['quantity']
            order_item = OrderItem.objects.create(product=prod,
                                                  order=order,
                                                  quantity=quantity)

    return JsonResponse({})
