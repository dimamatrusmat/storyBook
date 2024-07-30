from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from store.models import Category, Product


class TestBasketView(TestCase):
    def setUp(self):
        User.objects.create(username='admin')
        Category.objects.create(name='django', slug='django')
        Product.objects.create(category_id=1, title='JavaScript', created_by_id=1,
                               slug='javascript', price='20.00', image='javascript')
        Product.objects.create(category_id=1, title='Django', created_by_id=1,
                               slug='django', price='20.00', image='django')
        Product.objects.create(category_id=1, title='Django_Python', created_by_id=1,
                               slug='django_python', price='20.00', image='django_python')
        self.client.post(
            reverse('cart:basket_add'), {"productid": 1, "productqty": 1, "action": "post"}, xhr=True)
        self.client.post(
            reverse('cart:basket_add'), {"productid": 2, "productqty": 2, "action": "post"}, xhr=True)

    def test_basket_url(self):
        """
        Проверка статуса домашней страницы.
        """
        response = self.client.get(reverse('cart:cart_summary'))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        """
        Тестирование добавления товаров в корзину.
        """
        response = self.client.post(
            reverse('cart:basket_add'), {"productid": 3, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 4})
        response = self.client.post(
            reverse('cart:basket_add'), {"productid": 2, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 3})

    def test_basket_delete(self):
        """
        Тестирование удаления товаров из корзины.
        """
        response = self.client.post(
            reverse('cart:basket_delete'), {"productid": 2, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 1, 'subtotal': '20.00'})

    def test_basket_update(self):
        """
        Тестирование обнавления товаров в корзине.
        """
        response = self.client.post(
            reverse('cart:basket_update'), {"productid": 2, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 2, 'subtotal': '40.00'})
