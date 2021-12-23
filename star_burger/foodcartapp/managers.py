from django.db import models as m

from foodcartapp import models


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


class ProductQuerySet(m.QuerySet):
    def available(self):
        products = (models.RestaurantMenuItem.objects
                    .filter(availability=True)
                    .values_list('product'))

        return self.filter(pk__in=products)
