from django.contrib.auth import get_user_model

from art_project.accounts.models import Profile
from art_project.art_portal_app.models import Painting, Style, Technique, Gallery


UserModel = get_user_model()


class ArrangeMixin:
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
        'photo': 'monalisa.png',
        'price': 1000,
        'main_colors': 'blue'
    }

    def _create_valid_user_and_profile(self):
        # create user
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        # get the profile which is created automatically
        profile = Profile.objects.get(pk=user.pk)
        return user, profile

    def _create_other_user(self):
        user = UserModel.objects.create_user(**self.OTHER_USER_CREDENTIALS)
        # get the profile which is created automatically
        profile = Profile.objects.get(pk=user.pk)
        return user, profile

    def _create_style(self):
        style = Style.objects.create(style_name='Impressionism')
        return style

    def _create_technique(self):
        technique = Technique.objects.create(technique_name='Oil')
        return technique

    def _create_gallery(self):
        gallery = Gallery.objects.create(name='Maestro', address='Sofia')
        return gallery

    def _create_painting(self, user):
        style = self._create_style()
        technique = self._create_technique()
        gallery = self._create_gallery()
        painting = Painting.objects.create(
            **self.VALID_PAINTING_DATA, style=style, techniques=technique, gallery=gallery, artist=user)
        return painting
