from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from art_project.art_portal_app.forms import AddPaintingForm
from art_project.art_portal_app.models import Painting
from art_project.mixins import ArrangeMixin


UserModel = get_user_model()


class EditPaintingViewTests(ArrangeMixin, TestCase):

    def test_when_user_not_logged__expect_redirect_to_not_allowed(self):
        user, _ = self._create_valid_user_and_profile()
        painting = self._create_painting(user)

        response = self.client.get(reverse('edit painting', kwargs={'pk': painting.pk}))
        self.assertRedirects(response, reverse('not allowed'), status_code=302)

    def test_when_user_is_logged__expect_correct_template(self):
        user, _ = self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        painting = self._create_painting(user)

        response = self.client.get(reverse('edit painting', kwargs={'pk': painting.pk}))

        self.assertTemplateUsed(response, 'art_portal_templates/edit_painting.html')

    def test_when_user_is_logged_and_valid_data__expect_painting_updated(self):
        user, _ = self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        painting = self._create_painting(user)
        self._create_style()
        self._create_technique()
        self._create_gallery()
        updated_painting_data = {
            'title': 'Sunflowers',
            'width': 100,
            'height': 100,
            'base_material': Painting.CANVAS,
            'photo': 'monalisa.png',
            'price': 1000,
            'main_colors': 1,
            'style': 1,
            'techniques': 1,
            'gallery': 1,
        }

        self.client.post(reverse('edit painting', kwargs={'pk': painting.pk}), updated_painting_data)

        updated_painting = Painting.objects.first()

        self.assertEqual(updated_painting_data['title'], updated_painting.title)