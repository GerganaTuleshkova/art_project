from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from art_project.accounts.models import Profile
from art_project.accounts.tests.views.mixins import ArrangeMixin
from art_project.art_portal_app.models import Painting, Style, Technique, Gallery

UserModel = get_user_model()


class RegisterViewTests(ArrangeMixin, TestCase):

    def test__expect_correct_template_used(self):

        response = self.client.post(reverse('register'), self.VALID_USER_CREDENTIALS, follow=True)
        self.assertTemplateUsed(response, 'accounts_templates/register.html')

    def test_when_all_valid__expect_user_to_be_created_and_logged(self):
        response = self.client.post(reverse('register'), self.VALID_USER_CREDENTIALS, follow=True)
        users = UserModel.objects.all()
        self.assertTrue(response.context['user'])
        self.assertTrue(response.context['user'].is_authenticated)
