from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from art_project.accounts.models import Profile
from art_project.art_portal_app.models import Painting, Style, Technique, Gallery

UserModel = get_user_model()


class ProfileDetailsViewTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': 'asd123',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test.user@mail.com'
    }

    OTHER_USER_CREDENTIALS = {
        'username': 'otheruser',
        'password': 'asd123',
        'first_name': 'Other',
        'last_name': 'User',
        'email': 'other.user@mail.com'
    }

    VALID_PAINTING_DATA = {
        'title': 'Mona Lisa',
        'width': 100,
        'height': 100,
        'base_material': Painting.CANVAS,
        'photo': 'http://monalisa/url.png',
        'price': 1000,
        'main_colors': 'blue'
    }

    def __create_valid_user_and_profile(self):
        # create user
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        # get the profile which is created automatically
        profile = Profile.objects.get(pk=user.pk)
        return user, profile

    def __create_other_user(self):
        user = UserModel.objects.create_user(**self.OTHER_USER_CREDENTIALS)
        # get the profile which is created automatically
        profile = Profile.objects.get(pk=user.pk)
        return user, profile

    def __create_style(self):
        style = Style.objects.create(style_name='Impressionism')
        return style

    def __create_technique(self):
        technique = Technique.objects.create(technique_name='Oil')
        return technique

    def __create_gallery(self):
        gallery = Gallery.objects.create(name='Maestro', address='Sofia')
        return gallery

    def __create_painting(self, user):
        style = self.__create_style()
        technique = self.__create_technique()
        gallery = self.__create_gallery()
        painting = Painting.objects.create(
            **self.VALID_PAINTING_DATA, style=style, techniques=technique, gallery=gallery, artist=user)
        return painting

    def test_when_opening_not_existing_profile__expect_404(self):
        # no user created
        response = self.client.get(reverse('profile details', kwargs={'pk': 66}))
        self.assertEqual(404, response.status_code)

    def test__expect_correct_template_used(self):
        user, profile = self.__create_valid_user_and_profile()
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertTemplateUsed(response, 'accounts_templates/profile-details.html')

    def test_when_user_is_owner__expect_is_owner_to_be_true(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertTrue(response.context['is_owner'])

    def test_when_user_is_not_owner__expect_is_owner_to_be_false(self):
        # create the valid user & profile
        user, profile = self.__create_valid_user_and_profile()
        # create the other user & profile
        other_user, other_profile = self.__create_other_user()
        # login the other user
        self.client.login(**self.OTHER_USER_CREDENTIALS)
        # get the profile page for valid profile
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        # other user is not the owner of the profile details page
        self.assertFalse(response.context['is_owner'])

    def test_when_no_paintings__paintings_count_is_0(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertEqual(0, response.context['paintings_count'])

    def test_when_no_paintings__paintings_is_empty(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertEqual(0, len(response.context['paintings']))
        self.assertFalse(response.context['paintings'])

    def test_with_1_painting__expect_paintings_count_is_1(self):
        user, profile = self.__create_valid_user_and_profile()
        self.__create_painting(user)

        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertEqual(1, response.context['paintings_count'])

    def test_with_1_painting__expect_painting_is_the_painting(self):
        user, profile = self.__create_valid_user_and_profile()
        painting = self.__create_painting(user)

        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertIn(painting, response.context['paintings'])
        self.assertTrue(painting, response.context['paintings'][0])

    def test_with_2_paintings__expect_paintings_count_is_2(self):
        user, profile = self.__create_valid_user_and_profile()
        # create 1st painting
        self.__create_painting(user)
        # create 2nd painting
        self.__create_painting(user)

        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertEqual(2, response.context['paintings_count'])

    def test_with_1_painting_of_user_and_another_of_other_user__expect_painting_is_the_painting(self):
        user, profile = self.__create_valid_user_and_profile()
        other_user, other_profile = self.__create_other_user()
        painting = self.__create_painting(user)
        painting_of_other = self.__create_painting(other_user)

        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertIn(painting, response.context['paintings'])
        self.assertNotIn(painting_of_other, response.context['paintings'])
        self.assertEqual(1, response.context['paintings_count'])

