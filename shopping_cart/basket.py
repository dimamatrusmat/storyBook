from decimal import Decimal

from store.models import Product


class Basket():
    """
    Базовый класс корзины, предоставляющий некоторые параметры поведения по умолчанию, которые
    при необходимости могут быть унаследованы или переопределены.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, qty):
        """
        Добавление и обновление данных сеанса корзины пользователей.
        """
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}

        self.save()

    def __iter__(self):
        """
        Соберает product_id в данные сеанса, чтобы запросить базу
        данных и вернуть продукты.
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        """
        Получите данные о корзине и подсчитайте количество товаров.
        """
        return sum(item['qty'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def delete(self, product):
        """
        Удалить элемент из данных сеанса.
        """
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
        self.session.modified = True

    def update(self, product, qty):
        """
        Обновите значения в данных сеанса.
        """
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()

    def save(self):
        self.session.modified = True
