from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client
from .models import Category, Product


class AboutModelTests(TestCase):

    def setUp(self):
        # create a test user
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(
            username='hjansen',
            email='hj@email.com',
            password='ikhebkaas42',
        )

    def test_category_string_representation(self):
        """ test string representation of blog posts """
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        category = Category.objects.create(
            name="Test Category",
            friendly_name="Test Friendly Category"
        )
        self.assertEqual(str(category), category.name)

    def test_product_string_representation(self):
        """ test string representation of blog posts """
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        product = Product.objects.create(
            name="Test Product",
            description="Test description",
            ingredients="Test ingredients list",
            price=9.99,
            stock_qty=10,
            sold_qty=0,
        )
        self.assertEqual(str(product), product.name)
