from django.test import TestCase
from django.urls import reverse, resolve
from . import views

# Home App tests


class HomeAppTests(TestCase):

    def test_index_url(self):
        """ test index url/view set up correctly """
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.index)
