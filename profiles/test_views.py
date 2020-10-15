from django.contrib.auth.models import User
from django.test import Client, TestCase, RequestFactory
from .models import UserProfile
from .forms import UserProfileForm
from cart.models import Order


class ProfilesViewsTestsLoggedOut(TestCase):

    def setUp(self):
        self.client = Client()

    def test_response_redirect(self):
        """ test non-loggedin users redirected from profile to login """
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/profile/')


class ProfilesViewsTestsLoggedIn(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='hjansen', email='hj@email.com', password='ikhebkaas42'
        )

    def test_response_200(self):
        """ check user can access their profile """
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        response = client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_can_update_profile(self):
        """ check user can update their profile """
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        response = client.post(
            '/profile/',
            {
                'profile_full_name': 'Hans Jansen',
                'profile_phone_number': '07777777777',
                'profile_country': 'GB',
                'profile_postcode': 'CF10 1AS',
                'profile_town_or_city': 'Tywardreath',
                'profile-street_address1': '89 Caradon Hills',
                'profile_county': 'Cardyff',
            }
        )
        self.assertEqual(response.status_code, 200)
        user_profile = UserProfile.objects.get(user=self.user)
        form = UserProfileForm(response, instance=user_profile)
        self.assertTrue(form.is_valid())
        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_profile.profile_full_name, 'Hans Jansen')


class OrderHistoryViewsTestsLoggedOut(TestCase):

    def setUp(self):
        self.client = Client()

    def test_response_redirect(self):
        """ check user can't access profile if not logged in """
        response = self.client.get('/profile/order_history/123/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            '/accounts/login/?next=/profile/order_history/123/'
        )


class OrderHistoryViewsTestsLoggedIn(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='hjansen', email='hj@email.com', password='ikhebkaas42'
        )

    def test_response_200(self):
        """ check logged in user can access order history """
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        order = Order.objects.create(
            full_name='Hans Jansen',
            order_total=9.99,
            email='hj@email.com',
        )
        response = client.get(
            f'/profile/order_history/{order.order_reference}/'
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_access_order_history_if_old_email_confirmed(self):
        """ check logged in user can access order history made under a different
        email address if they confirm it first """
        order = Order.objects.create(
            full_name='Hans Jansen',
            order_total=9.99,
            email='hj-old@email.com',
        )
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        response = client.post(
            f'/profile/order_history/{order.order_reference}/',
            {
                'confirm-email': 'hj-old@email.com',
            }
        )
        context = response.context
        self.assertNotEqual(context['order'], None)
        self.assertEqual(context['order'], order)
        self.assertEqual(context['viewing_order_history'], True)
        self.assertEqual(response.status_code, 200)

    def test_user_must_confirm_order_history_with_different_email(self):
        """ check logged in user must confirm old email to access
        order history made under a different email address """
        order = Order.objects.create(
            full_name='Hans Jansen',
            order_total=9.99,
            email='hj-old@email.com',
        )
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        response = client.post(
            f'/profile/order_history/{order.order_reference}/',
            {
                'confirm-email': 'hj-incorrect@email.com',
            }
        )
        context = response.context
        self.assertEqual(context['order'], None)
        self.assertNotEqual(context['order'], order)
        self.assertEqual(response.status_code, 200)

    def test_user_cant_access_order_history_if_old_email_not_confirmed(self):
        """ check logged in user cannot access order history made under
         a different email address if they fail to confirm email """
        order = Order.objects.create(
            full_name='Hans Jansen',
            order_total=9.99,
            email='hj-old@email.com',
        )
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        response = client.get(
            f'/profile/order_history/{order.order_reference}/'
        )
        context = response.context
        self.assertEqual(context['order'], None)
        self.assertNotEqual(context['order'], order)
        self.assertEqual(response.status_code, 200)
