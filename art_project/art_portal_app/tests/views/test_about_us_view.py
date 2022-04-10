from django.test import TestCase
from django.urls import reverse


class AboutUsViewTests(TestCase):

    def test__expect_correct_template_used(self):
        response = self.client.post(reverse('about us'))
        self.assertTemplateUsed(response, 'art_portal_templates/about.html')
