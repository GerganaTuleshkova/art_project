from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from art_project.mixins import ArrangeMixin

UserModel = get_user_model()


class ProfileUpdateViewTests(ArrangeMixin, TestCase):

    def test__expect_correct_template_used(self):
        user, profile = self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('update profile'))
        self.assertTemplateUsed(response, 'accounts_templates/update_profile.html')

    def test_when_user_is_the_artist_expect_to_be_redirected_to_profile_details(self):
        user, profile = self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        post_response = self.client.post(reverse('update profile'), self.VALID_USER_CREDENTIALS, follow=True)

        self.assertRedirects(post_response, reverse('profile details', kwargs={'pk': profile.pk}), status_code=302)

    def test_when_user_is_not_login_expect_error(self):
        self._create_valid_user_and_profile()
        with self.assertRaises(Exception) as exc:
            self.client.post(reverse('update profile'), data=self.VALID_USER_CREDENTIALS, follow=True)

        self.assertIsNotNone(exc.exception)

    def test_when_user_is_the_artist_expect_profile_to_be_updated(self):
        self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.post(reverse('update profile'), data=self.OTHER_USER_CREDENTIALS, follow=True)

        updated_username = response.context['user'].username
        updated_first_name = response.context['user'].first_name
        self.assertEqual(self.OTHER_USER_CREDENTIALS['username'], updated_username)
        self.assertEqual(self.OTHER_USER_CREDENTIALS['first_name'], updated_first_name)



