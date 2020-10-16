from django.test import Client, TestCase, RequestFactory
from . import views
from cart.models import Order

# Home App tests


class HomeViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_response_200(self):
        """ test loading index page successful """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_loaded_templates(self):
        """ test index page loading correct templates """
        response = self.client.get('/')
        templates = response.templates
        names = fetch_template_names(templates)

        self.assertIn('base.html', str(names))
        self.assertIn('index.html', str(names))

    def test_track_order_correct_reference(self):
        """ test trying order tracking with correct reference number """
        test_order = Order.objects.create(
            order_reference='KOR-123ABC42',
            full_name='Hans Jansen',
            email='hj@test.com',
            phone_number='347777777777',
            town_or_city='Amsterdam',
            street_address1='Eerste Dijkstraat 622',
            street_address2='Watergraafsmere',
            county='Noord Holland',
            order_total='20.00',
            paid=True,
            stripe_pid='123',
        )
        request = self.factory.post(
            '/',
            {'order-ref-track': 'KOR-123ABC42'},
        )
        request.session = {}
        response = views.index(request)
        order_ref = request.POST['order-ref-track']
        track_order = Order.objects.get(
            order_reference=order_ref
        )
        self.assertEqual(test_order, track_order)
        self.assertEqual(response.status_code, 200)


# testing helper functions
def fetch_template_names(templates):
    template_names = []
    for t in templates:
        template_names.append(t.name)
    return template_names
