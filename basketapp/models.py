from django.db import models
from authapp.models import ShopUser
from mainapp.models import Product

from django.utils.functional import cached_property

# class BasketQuerySet(models.QuerySet):
#     def delete(self, *args, **kwargs):
#         print('Basket: query set DELETE METHOD works')
#         for object in self:
#             object.product.quantity += object.quantity
#             object.product.save()
#         super().delete(*args, **kwargs)


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(ShopUser, verbose_name='пользователь',
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='продукт',
                                on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время добавления', auto_now_add=True)

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    def _get_product_cost(self):
        # "return cost of all products this type"
        return self.product.price * self.quantity

    product_cost = property(_get_product_cost)

    @cached_property
    def get_items_cached(self):
        return self.user.basket_set.select_related()

    # def _get_total_quantity(self):
    #     # "return total quantity for user"
    #     # _items = Basket.objects.filter(user=self.user)
    #     _items = self.user.basket_set.all()
    #     _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
    #     return _totalquantity

    def get_total_quantity(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity, _items)))

    # def _get_total_cost(self):
    #     # "return total cost for user"
    #     _items = self.user.basket_set.all()
    #     _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
    #     return _totalcost

    def get_total_cost(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.product_cost, _items)))

    total_quantity = property(get_total_quantity)
    total_cost = property(get_total_cost)

    # def delete(self):
    #     print('Basket: own model DELETE METHOD works')
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete()

    # def save(self, *args, **kwargs):
    #     print('Basket: own model SAVE METHOD works')
    #     if self.pk:
    #         self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
    #     else:
    #         self.product.quantity -= self.quantity
    #         self.product.save()
    #     super().save(*args, **kwargs)
