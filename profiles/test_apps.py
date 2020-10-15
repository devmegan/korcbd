from django.test import TestCase
from . import apps


class ProfileAppTests(TestCase):

    def test_apps_config(self):
        """ test profiles app configured correctly"""
        self.assertEqual(apps.ProfilesConfig.name, 'profiles')
