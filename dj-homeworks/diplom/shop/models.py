from django.db import models
from django.db.models.signals import post_save


class Customers(models.Model):
    email = models.EmailField(max_length=64, unique=True, verbose_name='Эл.почта')
    password = models.CharField(max_length=20, verbose_name='Пароль')
    name = models.CharField(max_length=30, blank=True, null=True, default=None, verbose_name='Имя покупателя')
    surname = models.CharField(max_length=30, blank=True, null=True, default=None, verbose_name='Фамилия покупателя')
    phone = models.CharField(max_length=20, blank=True, null=True, default=None, verbose_name='Телефон')
    address = models.TextField(max_length=256, blank=True, null=True, default=None, verbose_name='Адрес покупателя')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
        
    class Meta:
        ordering = ['-id']
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class ProductCategory(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='Категория товара')
    description = models.TextField(blank=True, null=True, default=None, verbose_name='Статья')
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории товаров'


class ProductBrand(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Бренд')
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'



class Products(models.Model):
    name = models.CharField(max_length=64, verbose_name='Наименование товара')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name='Бренд')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')
    quantity = models.SmallIntegerField(default=0, verbose_name='Количество на складе')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Цена')
    short_text = models.CharField(max_length=128, blank=True, null=True, default=None, verbose_name='Краткое описание')
    description = models.TextField(blank=True, null=True, default=None, verbose_name='Описание')
    image = models.ImageField(upload_to='', verbose_name='Изображение')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата поступления')
    is_top = models.BooleanField(default=False, verbose_name = 'Топ')
    
    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ['name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Basket(models.Model):
    session_key = models.CharField(max_length=128, verbose_name='Ключ сессии')
    product = models.ForeignKey('Products', on_delete=models.CASCADE, verbose_name='Товар')
    number_of_units = models.SmallIntegerField(default=1, verbose_name='Количество')
#    price = models.ForeignKey('Products', verbose_name='Цена за единицу')
#    total_amount = models.DecimalField(verbose_name='Общая стоимость')
    
    class Meta:
        ordering = ['session_key', 'product']
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
    
    def __str__(self):
        return self.product.name
    
#    def save(self, *args, **kwargs):
#        self.price = self.product.price
#        self.total_amount = self.price * self.number_of_units
#        super(Basket, self).save(*args, **kwargs)

        

class Orders(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.SET('---'), verbose_name='Покупатель')
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
        ordering = ['created', 'status']
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

