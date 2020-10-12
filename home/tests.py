from django.test import Client, TestCase
from django.urls import reverse, resolve
from . import views

# Home App tests

class HomeAppTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_url(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.index)

    def test_response_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_loaded_templates(self):
        response = self.client.get('/')
        templates = response.templates
        names = fetch_template_names(templates)

        self.assertIn('base.html', str(names))
        self.assertIn('index.html', str(names))


# testing functions
def fetch_template_names(templates):
    template_names = []
    for t in templates:
        template_names.append(t.name)
    return template_names
