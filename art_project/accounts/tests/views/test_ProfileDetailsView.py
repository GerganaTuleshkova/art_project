from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from art_project.mixins import ArrangeMixin


UserModel = get_user_model()


class ProfileDetailsViewTests(ArrangeMixin, TestCase):

    def test_when_opening_not_existing_profile__expect_404(self):
        # no user created
        response = self.client.get(reverse('profile details', kwargs={'pk': 66}))
        self.assertEqual(404, response.status_code)

    def test__expect_correct_template_used(self):
        user, profile = self._create_valid_user_and_profile()
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertTemplateUsed(response, 'accounts_templates/profile-details.html')

    def test_when_user_is_owner__expect_is_owner_to_be_true(self):
        user, profile = self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertTrue(response.context['is_owner'])

    def test_when_user_is_not_owner__expect_is_owner_to_be_false(self):
        # create the valid user & profile
        user, profile = self._create_valid_user_and_profile()
        # create the other user & profile
        other_user, other_profile = self._create_other_user()
        # login the other user
        self.client.login(**self.OTHER_USER_CREDENTIALS)
        # get the profile page for valid profile
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        # other user is not the owner of the profile details page
        self.assertFalse(response.context['is_owner'])

    def test_when_no_paintings__paintings_count_is_0(self):
        user, profile = self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertEqual(0, response.context['paintings_count'])

    def test_when_no_paintings__paintings_is_empty(self):
        user, profile = self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertEqual(0, len(response.context['paintings']))
        self.assertFalse(response.context['paintings'])

    def test_with_1_painting__expect_paintings_count_is_1(self):
        user, profile = self._create_valid_user_and_profile()
        self._create_painting(user)

        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertEqual(1, response.context['paintings_count'])

    def test_with_1_painting__expect_painting_is_the_painting(self):
        user, profile = self._create_valid_user_and_profile()
        painting = self._create_painting(user)

        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertIn(painting, response.context['paintings'])
        self.assertTrue(painting, response.context['paintings'][0])

    def test_with_2_paintings__expect_paintings_count_is_2(self):
        user, profile = self._create_valid_user_and_profile()
        # create 1st painting
        self._create_painting(user)
        # create 2nd painting
        self._create_painting(user)

        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertEqual(2, response.context['paintings_count'])

    def test_with_1_painting_of_user_and_another_of_other_user__expect_painting_is_the_painting(self):
        user, profile = self._create_valid_user_and_profile()
        other_user, other_profile = self._create_other_user()
        painting = self._create_painting(user)
        painting_of_other = self._create_painting(other_user)

        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertIn(painting, response.context['paintings'])
        self.assertNotIn(painting_of_other, response.context['paintings'])
        self.assertEqual(1, response.context['paintings_count'])

