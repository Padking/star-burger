from django.db import models as m

from foodcartapp import models


class OrderQuerySet(m.QuerySet):

    def fetch_with_cost(self):
        prices_values_by_product = (m.F('items__quantity')
                                    * m.F('items__price'))

        orders_with_cost_field = self.annotate(cost=m.Sum(prices_values_by_product))

        return orders_with_cost_field


class ProductQuerySet(m.QuerySet):
    def available(self):
        products = (
            models.RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)
