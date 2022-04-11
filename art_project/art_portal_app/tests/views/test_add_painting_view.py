from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from art_project.art_portal_app.models import Painting
from art_project.mixins import ArrangeMixin

UserModel = get_user_model()


class PaintingAddViewTests(ArrangeMixin, TestCase):
    VALID_PAINTING_FULL_DATA = {
        'title': 'Mona Lisa',
        'width': 100,
        'height': 100,
        'base_material': Painting.CANVAS,
        'photo': SimpleUploadedFile(
            name='test_image.jpg',
            content=open('media/profile_pics/default.png', 'rb').read(),
            content_type='image/png'),
        'price': 1000,
        'main_colors': 1,
        'style': 1,
        'techniques': 1,
        'gallery': 1,
        'artist': 1,
    }

    def test_when_user_not_logged__expect_redirect_to_login_view_plus_next(self):
        # no user created
        response = self.client.get(reverse('add painting'))
        self.assertRedirects(response, reverse('login') + '?next=/painting/add/', status_code=302)

    def test__expect_correct_template_used(self):
        user, _ = self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('add painting'))

        self.assertTemplateUsed(response, 'art_portal_templates/add_painting.html')

    def test_with_valid_input_expect_redirect_to_painting_details(self):
        user, _ = self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        self._create_style()
        self._create_technique()
        self._create_gallery()
        response = self.client.post(reverse('add painting'), self.VALID_PAINTING_FULL_DATA)
        painting = Painting.objects.first()

        self.assertRedirects(response, reverse('painting details', kwargs={'pk': painting.pk}), status_code=302)

    def test_with_valid_input_expect_painting_to_be_added(self):
        user, _ = self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        self._create_style()
        self._create_technique()
        self._create_gallery()
        self.client.post(reverse('add painting'), self.VALID_PAINTING_FULL_DATA)
        painting = Painting.objects.first()

        self.assertEqual(self.VALID_PAINTING_FULL_DATA['title'], painting.title)
        self.assertEqual(1, len(Painting.objects.all()))
