from django.test import TestCase
from . import apps


class CartAppTests(TestCase):

    def test_apps_config(self):
        """ test about app configured correctly"""
        self.assertEqual(apps.CartConfig.name, 'cart')
