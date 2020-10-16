from django.contrib.auth.models import User
from django.test import Client, TestCase, RequestFactory
from .models import Product


class ProductsViewsTestsLoggedOut(TestCase):

    def setUp(self):
        self.client = Client()

    def test_response_200(self):
        """ test loading products page successful """
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_products_loaded_templates(self):
        """ test products page loading correct templates """
        response = self.client.get('/products/')
        templates = response.templates
        names = fetch_template_names(templates)
        self.assertIn('base.html', str(names))
        self.assertIn('products.html', str(names))

    def test_products_with_query_term(self):
        """ test loading products with a search query """
        response = self.client.get('/products/?search_q=test')
        context = response.context
        self.assertTrue(context['query_term'])
        self.assertFalse(context['category_name'])
        self.assertEqual(context['query_term'], 'test')

    def test_products_with_empty_query_term(self):
        """ test product search with empty query redirects to all products """
        response = self.client.get('/products/?search_q=')
        self.assertEqual(response.url, "/products/")

    def test_products_with_product_category(self):
        """ test loading products with a product category """
        response = self.client.get('/products/?category=test')
        context = response.context
        self.assertFalse(context['query_term'])
        self.assertTrue(context['category_name'])
        self.assertEqual(context['category_name'], 'test')

    def test_products_with_product_sortkey(self):
        """ test loading products with a directional sort """
        response = self.client.get(
            '/products/?category=test&sort=price&direction=desc'
        )
        context = response.context
        self.assertTrue(context['direction'])
        self.assertEqual(context['direction'], 'desc')


class ProductDetailViewsTestsLoggedOut(TestCase):

    def setUp(self):
        self.client = Client()

    def test_response_200(self):
        """ test loading product detail page successful """
        product = Product.objects.create(
            name="Test Product",
            description="Test description",
            ingredients="Test ingredients",
            price=29.99,
            stock_qty=1,
            sold_qty=0,
        )
        response = self.client.get(f'/products/product_detail/{product.id}/')
        self.assertEqual(response.status_code, 200)

    def test_product_in_product_detail_context(self):
        """ test product object is in product detail context """
        product = Product.objects.create(
            name="Test Product",
            description="Test description",
            ingredients="Test ingredients",
            price=29.99,
            stock_qty=1,
            sold_qty=0,
        )
        response = self.client.get(f'/products/product_detail/{product.id}/')
        context = response.context
        self.assertTrue(context['product'])
        self.assertEqual(context['product'].name, 'Test Product')

    def test_product_detail_loaded_templates(self):
        """ test product detail page loading correct templates """
        product = Product.objects.create(
            name="Test Product",
            description="Test description",
            ingredients="Test ingredients",
            price=29.99,
            stock_qty=1,
            sold_qty=0,
        )
        response = self.client.get(f'/products/product_detail/{product.id}/')
        templates = response.templates
        names = fetch_template_names(templates)
        self.assertIn('base.html', str(names))
        self.assertIn('product_detail.html', str(names))

    def test_add_product_login_required(self):
        """ test logged out users can't access add product page """
        response = self.client.get('/products/add_product/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/accounts/login/?next=/products/add_product/"
        )

    def test_edit_product_login_required(self):
        """ test logged out users can't access edit product page """
        response = self.client.get('/products/edit_product/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/accounts/login/?next=/products/edit_product/1/"
        )

    def test_delete_product_login_required(self):
        """ test logged out users can't access delete product page """
        response = self.client.get('/products/delete_product/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/accounts/login/?next=/products/delete_product/1/"
        )


class ProductViewsTestsNonSuperuser(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='hjansen', email='hj@email.com', password='ikhebkaas42'
        )

    def test_nonsuperuser_redirected_from_add_product(self):
        """ check nonsuperuser redirected from add product to home """
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        response = client.get('/products/add_product/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_nonsuperuser_redirected_from_edit_product(self):
        """ check nonsuperuser redirected from edit product to home """
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        response = client.get('/products/edit_product/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_nonsuperuser_redirected_from_delete_product(self):
        """ check nonsuperuser redirected from delete product to home """
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        response = client.get('/products/delete_product/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")


class ProductViewsTestsSuperuser(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(
            username='hjansen', email='hj@email.com', password='ikhebkaas42'
        )

    def test_superuser_can_reach_add_product(self):
        """ check superuser can reach add product page """
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        response = client.get('/products/add_product/')
        self.assertEqual(response.status_code, 200)

    def test_superuser_can_add_product(self):
        """ check superuser can add a product """
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        client.post(
            '/products/add_product/',
            {
                'name': 'Test Product',
                'description': 'Test description',
                'ingredients': 'Test ingredients',
                'price': 29.99,
                'stock_qty': 1,
                'sold_qty': 0,
            },
        )
        product = Product.objects.get(name='Test Product')
        self.assertTrue(product)
        self.assertEqual(product.description, 'Test description')

    def test_superuser_can_reach_edit_product(self):
        """ check superuser can reach edit product page """
        product = Product.objects.create(
            name='Test Product',
            description='Test description',
            ingredients='Test ingredients',
            price=29.99,
            stock_qty=1,
            sold_qty=0,
        )
        """ check superuser can add section to home """
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        response = client.get(f'/products/edit_product/{product.id}/')
        self.assertEqual(response.status_code, 200)

    def test_superuser_can_edit_product(self):
        """ check superuser can edit product """
        product = Product.objects.create(
            name="Test Product",
            description="Test description",
            ingredients="Test ingredients",
            price=29.99,
            stock_qty=1,
            sold_qty=0,
        )
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        client.post(
            f'/products/edit_product/{product.id}/',
            {
                'name': 'Updated Product',
                'description': 'Updated description',
                'ingredients': 'Updated ingredients',
                'price': 29.99,
                'stock_qty': 1,
                'sold_qty': 0,
            },
        )
        updated_product = Product.objects.get(id=product.id)
        self.assertTrue(updated_product)
        self.assertNotEqual(updated_product.name, product.name)
        self.assertNotEqual(updated_product.description, product.description)
        self.assertNotEqual(updated_product.ingredients, product.ingredients)
        self.assertEqual(updated_product.name, 'Updated Product')
        self.assertEqual(updated_product.description, 'Updated description')
        self.assertEqual(updated_product.ingredients, 'Updated ingredients')

    def test_superuser_can_delete_product(self):
        """ check superuser can delete an existing product """
        product = Product.objects.create(
            name='Test Product',
            description='Test description',
            ingredients='Test ingredients',
            price=29.99,
            stock_qty=1,
            sold_qty=0,
        )
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        response = client.get(f'/products/delete_product/{product.id}/')
        product = Product.objects.filter(id=product.id)
        self.assertFalse(product)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/products/")


# testing helper functions
def fetch_template_names(templates):
    template_names = []
    for t in templates:
        template_names.append(t.name)
    return template_names
