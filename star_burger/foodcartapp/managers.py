from collections import defaultdict

from django.conf import settings
from django.db import models as m
from geopy.distance import distance

from foodcartapp import models

from .utils import fetch_coordinates


class OrderQuerySet(m.QuerySet):

    def fetch_with_cost(self):
        prices_values_by_product = (
            m.F('items__quantity') * m.F('items__price')
        )

        orders_with_cost_field = self.annotate(cost=m.Sum(prices_values_by_product))

        return orders_with_cost_field

    def fetch_with_restaurant(self, querysets=None):

        querysets = querysets or []

        for order in self:
            for order_item in order.items.all():
                suitable_restaurants_ids_per_order_item = (order_item
                                                           .product.menu_items
                                                           .filter(availability=True)
                                                           .values_list('restaurant',
                                                                        flat=True))
                querysets.append(suitable_restaurants_ids_per_order_item)

            suitable_restaurants_ids_per_order = (suitable_restaurants_ids_per_order_item
                                                  .intersection(*querysets[:-1]))
            suitable_restaraunts = (models.Restaurant.objects
                                    .filter(id__in=suitable_restaurants_ids_per_order))
            order.restaurants = suitable_restaraunts
            querysets = []

        return self

    def fetch_with_distances(self, order_map_to_restaurant_and_distance=None):

        order_map_to_restaurant_and_distance = (
            order_map_to_restaurant_and_distance or defaultdict(list)
        )
        yandex_http_geocoder_api = settings.YANDEX_HTTP_GEOCODER_API

        for order in self:
            delivery_address_coords = fetch_coordinates(yandex_http_geocoder_api,
                                                        order.delivery_address)
            for restaurant in order.restaurants:
                restaurant_address_coords = fetch_coordinates(yandex_http_geocoder_api,
                                                              restaurant.address)
                try:
                    _distance = distance(delivery_address_coords,
                                         restaurant_address_coords).km
                except ValueError:
                    # Расстояние между точками вычислить не удалось
                    _distance = None
                order_map_to_restaurant_and_distance[order.pk].append((restaurant.name, _distance))

        sorted_by_distance = {order: sorted(restaurants_to_distance,
                                            key=lambda restaurant_to_distance: restaurant_to_distance[1])
                              for order, restaurants_to_distance
                              in order_map_to_restaurant_and_distance.items()}

        return sorted_by_distance


class ProductQuerySet(m.QuerySet):
    def available(self):
        products = (models.RestaurantMenuItem.objects
                    .filter(availability=True)
                    .values_list('product'))

        return self.filter(pk__in=products)
