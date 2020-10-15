from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client
from .models import UserProfile


class UserProfileModelTests(TestCase):

    def setUp(self):
        # create a test user
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='hjansen',
            email='hj@email.com',
            password='ikhebkaas42',
        )

    def test_profile_string_representation(self):
        """ test string representation of user profile """
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        user_profile = UserProfile.objects.get(
            user=self.user,
        )
        self.assertEqual(str(user_profile), self.user.username)
