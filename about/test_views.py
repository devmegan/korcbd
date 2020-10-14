from django.contrib.auth.models import User
from django.test import Client, TestCase, RequestFactory
from . import views
from . import forms
from .models import AboutSection

# Create your tests here.


class AboutViewsTestsLoggedOut(TestCase):

    def setUp(self):
        self.client = Client()

    def test_response_200(self):
        """ test loading about page successful """
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_about_loaded_templates(self):
        """ test about page loading correct templates """
        response = self.client.get('/about/')
        templates = response.templates
        names = fetch_template_names(templates)

        self.assertIn('base.html', str(names))
        self.assertIn('about.html', str(names))

    def test_add_section_login_required(self):
        """ test user redirected from add  section if not logged in """
        response = self.client.get('/about/add_section/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/accounts/login/?next=/about/add_section/"
        )

    def test_edit_section_login_required(self):
        """ test user redirected from edit section if not logged in """
        response = self.client.get('/about/edit_section/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/accounts/login/?next=/about/edit_section/1/"
        )

    def test_delete_section_login_required(self):
        """ test user redirected from delete section if not logged in"""
        response = self.client.get('/about/delete_section/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/accounts/login/?next=/about/delete_section/1/"
        )


class AboutViewsTestsNonSuperUser(TestCase):

    def setUp(self):
        # create a test user
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='hjansen', email='hj@email.com', password='ikhebkaas42')

    def test_nonsuperuser_redirected_from_add_section(self):
        """ check nonsuperuser redirected from add section to home """
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        # Create an instance of a GET request.
        response = client.get('/about/add_section/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_nonsuperuser_redirected_from_edit_section(self):
        """ check nonsuperuser redirected from edit section to home """
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        # Create an instance of a GET request.
        response = client.get('/about/edit_section/1/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_nonsuperuser_redirected_from_delete_section(self):
        """ check nonsuperuser redirected from delete section to home """
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        # Create an instance of a GET request.
        response = client.get('/about/delete_section/1/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")


class AboutViewsTestsSuperUser(TestCase):

    def setUp(self):
        # create a test user
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(
            username='hjansen',
            email='hj@email.com',
            password='ikhebkaas42',
        )

    def test_superuser_can_access_add_section(self):
        """ check superuser can access add section template """
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        response = client.get('/about/add_section/')
        self.assertEqual(response.status_code, 200)

        templates = response.templates
        names = fetch_template_names(templates)

        self.assertIn('add_section.html', str(names))
        self.assertIn('base.html', str(names))

    def test_superuser_can_add_section(self):
        """ check superuser can add section """
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        client.post(
            '/about/add_section/',
            {
                'section_title': 'Test Title',
                'body': 'Test body',
            },
        )
        section = AboutSection.objects.get(section_title='Test Title')
        self.assertEqual(section.section_title, 'Test Title')
        self.assertEqual(section.body, 'Test body')

    def test_superuser_loads_edit_section(self):
        """ test superuser can access edit section template """
        existing_section = AboutSection.objects.create(
            section_title="Existing Title",
            body="Existing body",
        )
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        response = client.get(f'/about/edit_section/{existing_section.id}/')
        self.assertEqual(response.status_code, 200)

        templates = response.templates
        names = fetch_template_names(templates)

        self.assertIn('edit_section.html', str(names))
        self.assertIn('base.html', str(names))

    def test_superuser_can_edit_section(self):
        """ check superuser can edit and existing about section """
        existing_section = AboutSection.objects.create(
            section_title="Existing Title",
            body="Existing body",
        )
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        client.post(
            f'/about/edit_section/{existing_section.id}/',
            {
                'section_title': 'Updated Title',
                'body': 'Updated body',
            },
        )
        section = AboutSection.objects.get(section_title='Updated Title')
        self.assertEqual(section.section_title, 'Updated Title')
        self.assertNotEqual(section.body, 'Test body')

    def test_superuser_can_delete_section(self):
        """ check superuser can delete existing about section """
        existing_section = AboutSection.objects.create(
            section_title="Existing Title",
            body="Existing body",
        )
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        response = client.get(f'/about/delete_section/{existing_section.id}/')
        self.assertRedirects(response, '/about/')
        existing_sections = AboutSection.objects.filter(id=existing_section.id)
        self.assertEqual(len(existing_sections), 0)


# testing helper functions
def fetch_template_names(templates):
    template_names = []
    for t in templates:
        template_names.append(t.name)
    return template_names
