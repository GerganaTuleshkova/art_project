from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from art_project.accounts.models import Profile
from art_project.accounts.tests.views.mixins import ArrangeMixin
from art_project.art_portal_app.models import Painting, Style, Technique, Gallery

UserModel = get_user_model()


class ProfileDeleteViewTests(ArrangeMixin, TestCase):
    # VALID_USER_CREDENTIALS = {
    #     'username': 'testuser',
    #     'password': 'asd123',
    #     'first_name': 'Test',
    #     'last_name': 'User',
    #     'email': 'test.user@mail.com'
    # }
    #
    # VALID_PAINTING_DATA = {
    #     'title': 'Mona Lisa',
    #     'width': 100,
    #     'height': 100,
    #     'base_material': Painting.CANVAS,
    #     'photo': 'monalisa.png',
    #     'price': 1000,
    #     'main_colors': 'blue'
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
    # def _create_valid_user_and_profile(self):
    #     # create user
    #     user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
    #     # get the profile which is created automatically
    #     profile = Profile.objects.get(pk=user.pk)
    #     return user, profile
    #
    # def _create_other_user(self):
    #     user = UserModel.objects.create_user(**self.OTHER_USER_CREDENTIALS)
    #     # get the profile which is created automatically
    #     profile = Profile.objects.get(pk=user.pk)
    #     return user, profile
    #
    # def _create_style(self):
    #     style = Style.objects.create(style_name='Impressionism')
    #     return style
    #
    # def _create_technique(self):
    #     technique = Technique.objects.create(technique_name='Oil')
    #     return technique
    #
    # def _create_gallery(self):
    #     gallery = Gallery.objects.create(name='Maestro', address='Sofia')
    #     return gallery
    #
    # def __create_painting(self, user):
    #     style = self._create_style()
    #     technique = self._create_technique()
    #     gallery = self._create_gallery()
    #     painting = Painting.objects.create(
    #         **self.VALID_PAINTING_DATA, style=style, techniques=technique, gallery=gallery, artist=user)
    #     return painting

    def test__expect_correct_template_used(self):
        user, profile = self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('delete profile', kwargs={'pk': profile.pk}))
        self.assertTemplateUsed(response, 'accounts_templates/delete_profile.html')

    def test_when_user_is_artist_expect_to_be_redirected_to_home(self):
        user, profile = self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        post_response = self.client.post(reverse('delete profile', kwargs={'pk': profile.pk}), follow=True)

        self.assertRedirects(post_response, reverse('home'), status_code=302)

    def test_when_user_is_not_the_artist_expect_to_be_redirected_to_not_allowed(self):
        user, profile = self._create_valid_user_and_profile()
        self._create_other_user()
        self.client.login(**self.OTHER_USER_CREDENTIALS)
        response = self.client.get(reverse('delete profile', kwargs={'pk': profile.pk}))
        self.assertRedirects(response, reverse('not allowed'), status_code=302)

    def test_when_user_is_artist_expect_to_be_deleted(self):
        user, profile = self._create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        users = UserModel.objects.all()
        profiles = Profile.objects.all()

        self.client.post(reverse('delete profile', kwargs={'pk': profile.pk}), follow=True)

        self.assertNotIn(user, users)
        self.assertNotIn(profile, profiles)

    def test_when_user_is_artist_and_has_painting_expect_painting_to_be_deleted(self):
        user, profile = self._create_valid_user_and_profile()
        painting = self._create_painting(user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        paintings = Painting.objects.all()
        paintings_of_user = paintings.filter(artist=user.pk)

        self.client.post(reverse('delete profile', kwargs={'pk': profile.pk}), follow=True)

        self.assertFalse(paintings_of_user)
        self.assertNotIn(painting, paintings)
