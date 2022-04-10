from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from art_project.mixins import ArrangeMixin


UserModel = get_user_model()


class PaintingDetailsViewTests(ArrangeMixin, TestCase):

    def test_when_opening_not_existing_painting__expect_404(self):
        # no user created
        response = self.client.get(reverse('painting details', kwargs={'pk': 66}))
        self.assertEqual(404, response.status_code)

    def test__expect_correct_template_used(self):
        user, _ = self._create_valid_user_and_profile()
        painting = self._create_painting(user)

        response = self.client.get(reverse('painting details', kwargs={'pk': painting.pk}))
        self.assertTemplateUsed(response, 'art_portal_templates/painting_details.html')

    def test_when_user_is_owner__expect_is_author_to_be_true(self):
        user, _ = self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        painting = self._create_painting(user)

        response = self.client.get(reverse('painting details', kwargs={'pk': painting.pk}))

        self.assertTrue(response.context['is_author'])

    def test_when_user_is_not_owner__expect_is_author_to_be_false(self):
        # create the valid user & profile
        user, profile = self._create_valid_user_and_profile()
        painting = self._create_painting(user)
        # create the other user & profile
        other_user, other_profile = self._create_other_user()
        # login the other user
        self.client.login(**self.OTHER_USER_CREDENTIALS)

        response = self.client.get(reverse('painting details', kwargs={'pk': painting.pk}))

        self.assertFalse(response.context['is_author'])