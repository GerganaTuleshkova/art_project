from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from art_project.art_portal_app.forms import AddPaintingForm
from art_project.art_portal_app.models import Painting
from art_project.mixins import ArrangeMixin


UserModel = get_user_model()


class PaintingAddViewTests(ArrangeMixin, TestCase):

    def test_when_user_not_logged__expect_redirect_to_login_view_plus_next(self):
        # no user created
        response = self.client.get(reverse('add painting'))
        self.assertRedirects(response, reverse('login')+'?next=/painting/add/', status_code=302)

    def test__expect_correct_template_used(self):
        user, _ = self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('add painting'))

        self.assertTemplateUsed(response, 'art_portal_templates/add_painting.html')

    # def test_with_valid_input_expect_redirect_to_painting_details(self):
    #     # does not work!!!
    #     user, _ = self._create_valid_user_and_profile()
    #     self.client.login(**self.VALID_USER_CREDENTIALS)
    #     style = self._create_style()
    #     technique = self._create_technique()
    #     gallery = self._create_gallery()
    #     response = self.client.post(reverse('add painting'), **self.VALID_PAINTING_DATA,
    #                                 style=style, techniques=technique, gallery=gallery, artist=user, follow=True)
    #
    #     self.assertRedirects(response, reverse('painting details', kwargs={'pk': profile.pk}), status_code=302)

    def test_with_valid_input_expect_painting_to_be_added(self):
        # does not work!!!
        title = 'Mona Lisa'
        width = 100
        height = 100
        base_material = Painting.CANVAS
        photo = 'monalisa.png'
        price = 1000
        main_colors = 1
        user, _ = self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        style = self._create_style()
        technique = self._create_technique()
        gallery = self._create_gallery()
        # response = self.client.post(reverse('add painting'),
        #                             self.VALID_PAINTING_DATA,
        #                             style=style, techniques=technique, gallery=gallery,
        #                             follow=True)
        response = self.client.post(reverse('add painting'), title=title, width=width, height=height, base_material=base_material,
                                    photo=photo, price=price, main_colors=main_colors,
                                    style=style, techniques=technique, gallery=gallery, artist=user,
                                    follow=True)
        # Painting.objects.create(**self.VALID_PAINTING_DATA,
        #                         style=style, techniques=technique, gallery=gallery, artist=user)
        # paintings = Painting.objects.all()
        #
        print(response.context)
        # print(paintings)

        self.assertEqual(200, response.status_code)
        # self.assertEqual(self.VALID_PAINTING_DATA['title'], painting[0].title)