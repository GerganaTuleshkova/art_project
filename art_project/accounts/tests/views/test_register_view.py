from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from art_project.accounts.forms import UserRegisterForm
from art_project.mixins import ArrangeMixin

UserModel = get_user_model()


class RegisterViewTests(ArrangeMixin, TestCase):

    def test__expect_correct_template_used(self):

        response = self.client.post(reverse('register'), self.VALID_USER_CREDENTIALS, follow=True)
        self.assertTemplateUsed(response, 'accounts_templates/register.html')
        self.failUnless(isinstance(response.context['form'], UserRegisterForm))

    # def test_when_all_valid__expect_user_to_be_created_and_logged(self):
    #     # does not work !!!
    #     response = self.client.post(reverse('register'), self.VALID_USER_CREDENTIALS, follow=True)
    #     users_count = UserModel.objects.count()
    #
    #     self.assertEqual(1, users_count)
    #
    # def test_valid_credentials__expect_to_be_redirected_to_home(self):
    #     # does not work !!!
    #     response = self.client.post(reverse('register'), self.VALID_USER_CREDENTIALS, follow=True)
    #     user = response.context['user']
    #
    #     self.assertRedirects(response, reverse('profile details', kwargs={'pk': user.pk}), status_code=302)
