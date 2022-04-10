from django.test import TestCase
from django.urls import reverse


class NotAllowedViewTests(TestCase):

    def test__expect_correct_template_used(self):
        response = self.client.post(reverse('not allowed'))
        self.assertTemplateUsed(response, 'art_portal_templates/not_allowed.html')
