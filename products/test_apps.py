from django.test import TestCase
from . import apps


class ProductAppTests(TestCase):

    def test_apps_config(self):
        """ test products app configured correctly"""
        self.assertEqual(apps.ProductsConfig.name, 'products')
