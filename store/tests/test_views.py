from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse
from django.conf import settings
from importlib import import_module

from store.models import Category, Product
from store.views import products_all


class TestViewResponse(TestCase):

    def setUp(self):
        self.c = Client()
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='admin')
        Product.objects.create(
            category_id=1, title='django beginners', created_by_id=1,
            slug='django-beginners', price='20.00', image='gjango')

    def test_url_allowed_host(self):
        """
        Тест разрешенного хоста
        """
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.c.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)

    def test_product_detail_url(self):
        """
        Тестирование URL модели Product
        """
        response = self.c.get(reverse(
            'store:product_detail', args=['django-beginners']))
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        """
        Тестирование URL модели Category
        """
        response = self.c.get(reverse('store:category_list', args=['django']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """
        Тестирования шаблона home
        """
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = products_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>BookStore</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)
