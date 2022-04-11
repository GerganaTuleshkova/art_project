from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from art_project.mixins import ArrangeMixin

UserModel = get_user_model()


class UserLoginViewTests(TestCase, ArrangeMixin):

    def test__expect_correct_template(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed('accounts_templates/login.html')

    def test_valid_credentials__expect_successful_login(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        response = self.client.post(reverse('login'), self.VALID_USER_CREDENTIALS, follow=True)

        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(user, response.context['user'])

    def test_valid_credentials__expect_successful_login_not_other_user(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        other_user = UserModel.objects.create_user(**self.OTHER_USER_CREDENTIALS)
        response = self.client.post(reverse('login'), self.VALID_USER_CREDENTIALS, follow=True)

        self.assertNotEqual(other_user, response.context['user'])

    def test_valid_credentials__expect_to_be_redirected_to_home(self):
        UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        response = self.client.post(reverse('login'), self.VALID_USER_CREDENTIALS, follow=True)

        self.assertRedirects(response, reverse('home'), status_code=302)

    def test_invalid_credentials__expect_reload(self):
        UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        response = self.client.post(reverse('login'), self.OTHER_USER_CREDENTIALS, follow=True)

        self.assertEqual(200, response.status_code)
