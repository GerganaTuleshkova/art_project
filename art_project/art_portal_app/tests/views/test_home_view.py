from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):

    def test__expect_correct_template_used(self):
        response = self.client.post(reverse('home'))
        self.assertTemplateUsed(response, 'art_portal_templates/home.html')
