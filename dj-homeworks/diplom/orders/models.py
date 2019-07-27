from django.db import models
from django.db.models.signals import post_save
from shop.models import Customers


class Orders(models.Model):
    customer = models.ForeignKey(Customers, null=True, on_delete=models.SET_NULL, verbose_name='Покупатель')
    comments = models.TextField(blank=True, null=True, default=None, verbose_name='Комментарий к заказу')
    total_number = models.SmallIntegerField(default=1, verbose_name='Общее количество')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Общая стоимость')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Последнее изменение')

    ORDER_STATUS = (
        (1, 'Новый'),
        (2, 'Оплачено'),
        (3, 'Выполняется'),
        (4, 'Отправлен'),
        (5, 'Выполнен'),
        (6, 'Отменён'),

    )
    status = models.SmallIntegerField(choices=ORDER_STATUS, default=1, verbose_name='Статус заказа')

    class Meta:
        ordering = ['-created', 'status']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ: {self.id}'


class ProductsInOrder(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.CharField(max_length=64, verbose_name='Товар')
    number_of_units = models.SmallIntegerField(default=1, verbose_name='Количество')
    price_of_unit = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Цена за единицу')
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Общая стоимость')

    class Meta:
        ordering = ['product']
        verbose_name = 'Товар'
        verbose_name_plural = 'Заказанные товары'

    def __str__(self):
        return self.product

    def save(self, *args, **kwargs):
        self.total_amount = self.price_of_unit * self.number_of_units
        super(ProductsInOrder, self).save(*args, **kwargs)


def save_order(sender, instance, created, **kwargs):
    products_in_order = ProductsInOrder.objects.filter(order=instance.order)
    order_total_price = 0
    total_number = 0
    for unit in products_in_order:
        order_total_price += unit.total_amount
        total_number += unit.number_of_units
    instance.order.total_price = order_total_price
    instance.order.total_number = total_number
    instance.order.save(force_update=True)


post_save.connect(save_order, sender=ProductsInOrder)
