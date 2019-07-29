from decimal import Decimal


class Cart(object):
    """ Класс для работы с корзиной покупателя через сессии """

    def __init__(self, request):
        """ Инициализация корзины покупателя """
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def __iter__(self):
        for key, item in self.cart.items():
            item['id'] = key
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1):
        """ Добавление товара в корзину и обновление количества товара """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        self.cart[product_id]['quantity'] = quantity
        self.cart[product_id]['image'] = str(product.image)
        self.cart[product_id]['name'] = product.name
        self.cart[product_id]['prod_quantity'] = product.quantity

        self.save()

    def save(self):
        """ Сохраняем данные в сесию. """
        self.session['cart'] = self.cart
        self.session.modified = True

    def remove(self, product):
        """ Удаление продукта из корзины """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """ Полная очистка корзины """
        del self.session['cart']
        self.session.modified = True

    def get_product_quantity(self, product_id):
        """
        Функция возвращает количество конкретного товара. Вызывается на странице детального
        описания товара. Если в корзине данного товара нет, в поле: 'количество_товара_для_заказа'
        пишется 1.
        """
        if product_id in self.cart:
            return self.cart[product_id]['quantity']
        else:
            return 1

    def get_total_quantity(self):
        """ Получить общее количество товаров в корзине """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """ Получить общую стоимость товаров в корзине """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
