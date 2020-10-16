from django.contrib.auth.models import User
from django.test import Client, TestCase, RequestFactory
from products.models import Product
from cart.contexts import cart_contents


class CartViewsTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_response_200(self):
        """ test cart page loads successfully """
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)

    def test_empty_cart_initialised_in_context(self):
        response = self.client.get('/cart/')
        context = response.context
        self.assertEqual(context['cart_items'], [])

    def test_adding_new_product_to_cart(self):
        """ test user can add qty of product to their cart """
        client = Client()
        product = Product.objects.create(
            name='Test Product',
            price=9.99,
            stock_qty=10,
        )
        response = client.post(
            f'/cart/add_to_cart/{product.id}/',
            {
                'quantity': 2,
                'redirect_url': '/cart/'
            }
        )
        response = client.get('/cart/')
        context = response.context
        self.assertNotEqual(context['cart_items'], [])
        self.assertEqual(
            context['cart_items'][0]['product_id'],
            f'{product.id}'
        )

    def test_increasing_product_qty_in_cart(self):
        """ test user can increase qty of product in their cart """
        client = Client()
        product = Product.objects.create(
            name='Test Product',
            price=9.99,
            stock_qty=10,
        )
        response = client.post(
            f'/cart/add_to_cart/{product.id}/',
            {
                'quantity': 2,
                'redirect_url': '/cart/'
            }
        )
        # add second qty of same product to cart
        response = client.post(
            f'/cart/add_to_cart/{product.id}/',
            {
                'quantity': 2,
                'redirect_url': '/cart/'
            }
        )
        response = client.get('/cart/')
        context = response.context
        self.assertNotEqual(context['cart_items'], [])
        self.assertNotEqual(context['cart_items'][0]['quantity'], 2)
        self.assertEqual(context['cart_items'][0]['quantity'], 4)

    def test_adding_product_qty_cant_exceed_stock_qty_in_cart(self):
        """ test user cant add product to cart in qty that exceeds
        the product stock qty """
        client = Client()
        product = Product.objects.create(
            name='Test Product',
            price=9.99,
            stock_qty=10,
        )
        response = client.post(
            f'/cart/add_to_cart/{product.id}/',
            {
                'quantity': 20,
                'redirect_url': '/cart/'
            }
        )
        response = client.get('/cart/')
        context = response.context
        self.assertEqual(context['cart_items'], [])

    def test_increasing_product_qty_cant_exceed_stock_qty_in_cart(self):
        """ test user can increase qty of product in their cart """
        client = Client()
        product = Product.objects.create(
            name='Test Product',
            price=9.99,
            stock_qty=10,
        )
        response = client.post(
            f'/cart/add_to_cart/{product.id}/',
            {
                'quantity': 9,
                'redirect_url': '/cart/'
            }
        )
        response = client.post(
            f'/cart/add_to_cart/{product.id}/',
            {
                'quantity': 11,
                'redirect_url': '/cart/'
            }
        )
        response = client.get('/cart/')
        context = response.context
        self.assertNotEqual(context['cart_items'], [])
        self.assertNotEqual(context['cart_items'][0]['quantity'], 20)
        self.assertEqual(context['cart_items'][0]['quantity'], 9)

    def test_cart_can_be_update_from_cart_view(self):
        client = Client()
        product = Product.objects.create(
            name='Test Product',
            price=9.99,
            stock_qty=10,
        )
        # add product to cart so it can be updated
        client.post(
            f'/cart/add_to_cart/{product.id}/',
            {
                'quantity': 2,
                'redirect_url': '/cart/'
            }
        )
        # reduce qty of product in cart
        client.post(
            f'/cart/update/{product.id}/',
            {
                'quantity': 1,
                'redirect_url': '/cart/'
            }
        )
        response = client.get('/cart/')
        context = response.context
        self.assertNotEqual(context['cart_items'], [])
        self.assertNotEqual(context['cart_items'][0]['quantity'], 2)
        self.assertEqual(context['cart_items'][0]['quantity'], 1)

    def test_product_in_cart_cant_be_increased_past_stock_qty(self):
        client = Client()
        product = Product.objects.create(
            name='Test Product',
            price=9.99,
            stock_qty=10,
        )
        # add product to cart so it can be updated
        client.post(
            f'/cart/add_to_cart/{product.id}/',
            {
                'quantity': 2,
                'redirect_url': '/cart/'
            }
        )
        # increase qty of product in cart past stock qty
        client.post(
            f'/cart/update/{product.id}/',
            {
                'quantity': 12,
                'redirect_url': '/cart/'
            }
        )
        response = client.get('/cart/')
        context = response.context
        self.assertTrue(context['message'])
        self.assertEqual(context['cart_items'][0]['quantity'], 10)
        self.assertNotEqual(context['cart_items'][0]['quantity'], 12)
        self.assertNotEqual(context['cart_items'][0]['quantity'], 2)

    def test_product_can_be_removed_from_cart_by_0_qty(self):
        client = Client()
        product = Product.objects.create(
            name='Test Product',
            price=9.99,
            stock_qty=10,
        )
        # add product to cart so it can be updated
        client.post(
            f'/cart/add_to_cart/{product.id}/',
            {
                'quantity': 2,
                'redirect_url': '/cart/'
            }
        )
        # reduce qty of product in cart
        client.post(
            f'/cart/update/{product.id}/',
            {
                'quantity': 0,
                'redirect_url': '/cart/'
            }
        )
        response = client.get('/cart/')
        context = response.context
        self.assertEqual(context['cart_items'], [])

    def test_product_can_be_removed_from_cart_by_delete_view(self):
        client = Client()
        product = Product.objects.create(
            name='Test Product',
            price=9.99,
            stock_qty=10,
        )
        # add product to cart so it can be updated
        client.post(
            f'/cart/add_to_cart/{product.id}/',
            {
                'quantity': 2,
                'redirect_url': '/cart/'
            }
        )
        # reduce qty of product in cart
        client.get(
            f'/cart/remove/{product.id}/',
        )
        response = client.get('/cart/')
        context = response.context
        self.assertEqual(context['cart_items'], [])

    def test_exception_when_removing_from_cart_by_delete_view(self):
        client = Client()
        product = Product.objects.create(
            name='Test Product',
            price=9.99,
            stock_qty=10,
        )
        # add product to cart so it can be updated
        client.post(
            f'/cart/add_to_cart/{product.id}/',
            {
                'quantity': 2,
                'redirect_url': '/cart/'
            }
        )
        # force exception block to run due to nonexisting product id
        client.get('/cart/remove/99/')
        response = client.get('/cart/')
        context = response.context
        self.assertNotEqual(context['cart_items'], [])
        self.assertEqual(context['cart_items'][0]['product_id'], '1')