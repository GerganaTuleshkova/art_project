from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from art_project.accounts.models import Profile
from art_project.accounts.tests.views.mixins import ArrangeMixin
from art_project.art_portal_app.models import Painting, Style, Technique, Gallery

UserModel = get_user_model()


class RegisterViewTests(TestCase, ArrangeMixin):
    # VALID_USER_CREDENTIALS = {
    #     'username': 'testuser',
    #     'password': 'asd123',
    #     'first_name': 'Test',
    #     'last_name': 'User',
    #     'email': 'test.user@mail.com'
    # }
    #
    # OTHER_USER_CREDENTIALS = {
    #     'username': 'otheruser',
    #     'password': 'asd123',
    #     'first_name': 'Other',
    #     'last_name': 'User',
    #     'email': 'other.user@mail.com'
    # }
    #
    # VALID_PAINTING_DATA = {
    #     'title': 'Mona Lisa',
    #     'width': 100,
    #     'height': 100,
    #     'base_material': Painting.CANVAS,
    #     'photo': 'http://monalisa/url.png',
    #     'price': 1000,
    #     'main_colors': 'blue'
    # }
    #
    # def __create_valid_user_and_profile(self):
    #     # create user
    #     user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
    #     # get the profile which is created automatically
    #     profile = Profile.objects.get(pk=user.pk)
    #     return user, profile
    #
    # def __create_other_user(self):
    #     user = UserModel.objects.create_user(**self.OTHER_USER_CREDENTIALS)
    #     # get the profile which is created automatically
    #     profile = Profile.objects.get(pk=user.pk)
    #     return user, profile
    #
    # def __create_style(self):
    #     style = Style.objects.create(style_name='Impressionism')
    #     return style
    #
    # def __create_technique(self):
    #     technique = Technique.objects.create(technique_name='Oil')
    #     return technique
    #
    # def __create_gallery(self):
    #     gallery = Gallery.objects.create(name='Maestro', address='Sofia')
    #     return gallery
    #
    # def __create_painting(self, user):
    #     style = self.__create_style()
    #     technique = self.__create_technique()
    #     gallery = self.__create_gallery()
    #     painting = Painting.objects.create(
    #         **self.VALID_PAINTING_DATA, style=style, techniques=technique, gallery=gallery, artist=user)
    #     return painting

    def test__expect_correct_template_used(self):

        response = self.client.post(reverse('register'), self.VALID_USER_CREDENTIALS, follow=True)
        self.assertTemplateUsed(response, 'accounts_templates/register.html')

    def test_when_all_valid__expect_user_to_be_created_and_logged(self):
        response = self.client.post(reverse('register'), self.VALID_USER_CREDENTIALS, follow=True)
        users = UserModel.objects.all()
        self.assertTrue(response.context['user'])
        self.assertTrue(response.context['user'].is_authenticated)
