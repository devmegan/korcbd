from django.test import TestCase
from .models import AboutSection


class AboutModelTests(TestCase):

    def test_string_representation(self):
        section = AboutSection(section_title="Test Section")
        self.assertEqual(str(section), section.section_title)
