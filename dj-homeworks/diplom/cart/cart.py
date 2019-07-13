from decimal import Decimal
from shop.models import Products


class Cart(object):
    def __init__(self, request):
        """ Инициализация корзины покупателя """
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """ Добавление товара в корзину и обновление количества товара """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id]['quantity'] = quantity
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
        del self.session['cart']
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Products.objects.filter(pk__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_product_quantity(self, product_id):
        """ Получить количество конкретного товара """
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
