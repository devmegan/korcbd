from django.test import TestCase
from . import apps


class HomeAppTests(TestCase):

    def test_apps_config(self):
            """ test home app configured correctly"""
            self.assertEqual(apps.HomeConfig.name, 'home')