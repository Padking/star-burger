from collections import defaultdict

from django.db import models
from geopy.distance import distance

from foodcartapp import models as foodcart_models
from loccoder import models as loccoder_models

from loccoder.utils import get_obj_from_db


class OrderQuerySet(models.QuerySet):

    def fetch_with_cost(self):
        prices_values_by_product = (
            models.F('items__quantity') * models.F('items__price')
        )

        orders_with_cost_field = self.annotate(cost=models.Sum(prices_values_by_product))

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
            suitable_restaraunts = (foodcart_models.Restaurant.objects
                                    .filter(id__in=suitable_restaurants_ids_per_order))
            order.restaurants = suitable_restaraunts
            querysets = []

        return self

    def fetch_with_distances(self, order_map_to_restaurant_and_distance=None):

        order_map_to_restaurant_and_distance = (
            order_map_to_restaurant_and_distance or defaultdict(list)
        )

        locations = loccoder_models.Location.objects.all()

        for order in self:
            order_location = get_obj_from_db(locations, order.delivery_address)

            for restaurant in order.restaurants:
                restaurant_location = get_obj_from_db(locations, restaurant.address)

                delivery_address_coords = (
                    order_location.latitude, order_location.longitude
                )
                restaurant_address_coords = (
                    restaurant_location.latitude, restaurant_location.longitude
                )

                try:
                    _distance = distance(delivery_address_coords,
                                         restaurant_address_coords).km
                except ValueError:
                    # Расстояние между точками вычислить не удалось
                    _distance = None
                order_map_to_restaurant_and_distance[order.pk].append((
                    restaurant.name, _distance
                ))

        sorted_by_distance = {order: sorted(restaurants_to_distance,
                                            key=lambda restaurant_to_distance: restaurant_to_distance[1])
                              for order, restaurants_to_distance
                              in order_map_to_restaurant_and_distance.items()}

        return sorted_by_distance


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (foodcart_models.RestaurantMenuItem.objects
                    .filter(availability=True)
                    .values_list('product'))

        return self.filter(pk__in=products)
