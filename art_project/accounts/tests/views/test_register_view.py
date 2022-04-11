from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from art_project.accounts.forms import UserRegisterForm
from art_project.accounts.models import Profile
from art_project.mixins import ArrangeMixin

UserModel = get_user_model()


class RegisterViewTests(ArrangeMixin, TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password1': 'asd123hrjstl&^',
        'password2': 'asd123hrjstl&^',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test.user@mail.com'
    }

    def test__expect_correct_template_used(self):

        response = self.client.post(reverse('register'), self.VALID_USER_CREDENTIALS, follow=True)
        self.assertTemplateUsed(response, 'accounts_templates/register.html')
        self.failUnless(isinstance(response.context['form'], UserRegisterForm))

    def test_when_all_valid__expect_user_to_be_created_and_logged(self):
        response = self.client.post(reverse('register'), self.VALID_USER_CREDENTIALS, follow=True)

        users_count = UserModel.objects.count()
        user_created = UserModel.objects.first()

        self.assertEqual(1, users_count)
        self.assertEqual(self.VALID_USER_CREDENTIALS['username'], user_created.username)
        self.assertEqual(user_created, response.context['user'])

    def test_valid_credentials__expect_to_be_redirected_to_home(self):
        response = self.client.post(reverse('register'), self.VALID_USER_CREDENTIALS, follow=True)
        user_created = UserModel.objects.first()

        self.assertRedirects(response, reverse('profile details', kwargs={'pk': user_created.pk}), status_code=302)

    def test_when_all_valid__expect_profile_to_be_created(self):
        self.client.post(reverse('register'), self.VALID_USER_CREDENTIALS, follow=True)

        profile = Profile.objects.first()

        self.assertEqual(self.VALID_USER_CREDENTIALS['first_name'], profile.first_name)
        self.assertEqual(self.VALID_USER_CREDENTIALS['last_name'], profile.last_name)
