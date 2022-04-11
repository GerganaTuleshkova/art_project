from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from art_project.art_portal_app.models import Painting
from art_project.mixins import ArrangeMixin


UserModel = get_user_model()


class DeletePaintingViewTests(ArrangeMixin, TestCase):

    def test_when_user_not_logged__expect_redirect_to_not_allowed(self):
        user, _ = self._create_valid_user_and_profile()
        painting = self._create_painting(user)

        response = self.client.get(reverse('delete painting', kwargs={'pk': painting.pk}))
        self.assertRedirects(response, reverse('not allowed'), status_code=302)

    def test_when_user_is_logged__expect_correct_template(self):
        user, _ = self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        painting = self._create_painting(user)

        response = self.client.get(reverse('delete painting', kwargs={'pk': painting.pk}))

        self.assertTemplateUsed(response, 'art_portal_templates/delete_painting.html')

    def test_when_all_valid__expect_redirect_to_profile_details(self):
        user, _ = self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        painting = self._create_painting(user)

        response = self.client.post(reverse('delete painting', kwargs={'pk': painting.pk}))

        self.assertRedirects(response, reverse('profile details', kwargs={'pk': user.pk}), status_code=302)

    def test_when_all_valid__expect_painting_to_be_deleted(self):
        user, _ = self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        painting = self._create_painting(user)

        self.client.post(reverse('delete painting', kwargs={'pk': painting.pk}))
        paintings = Painting.objects.all()

        self.assertEqual(0, len(paintings))