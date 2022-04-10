from django.test import TestCase
from django.urls import reverse


class InternalErrorViewTests(TestCase):

    def test__expect_correct_template_used(self):
        response = self.client.post(reverse('internal error'))
        self.assertTemplateUsed(response, 'art_portal_templates/error.html')
