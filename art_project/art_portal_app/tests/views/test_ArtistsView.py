from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from art_project.mixins import ArrangeMixin

UserModel = get_user_model()


class ArtistsViewTests(ArrangeMixin, TestCase):

    def test__expect_correct_template_used(self):
        response = self.client.get(reverse('artists'))
        self.assertTemplateUsed(response, 'art_portal_templates/artists.html')

    def test_artists_with_no_paintings__expect_no_artist_in_context(self):
        self._create_valid_user_and_profile()
        self._create_other_user()

        response = self.client.get(reverse('artists'))
        artists_with_paintings_counts = len(response.context['artists'])
        self.assertEqual(0, artists_with_paintings_counts)

    def test_artists_with_2_paintings__expect_both_artists_in_context(self):
        # create 1st artist and his painting
        user, profile = self._create_valid_user_and_profile()
        self._create_painting(user)
        # create 2nd artists and his painting
        other_user, other_profile = self._create_other_user()
        self._create_painting(other_user)

        response = self.client.get(reverse('artists'))
        artists_with_paintings_counts = len(response.context['artists'])
        self.assertEqual(2, artists_with_paintings_counts)
        self.assertIn(profile, response.context['artists'])
        self.assertIn(other_profile, response.context['artists'])

    def test_one_artist_with_painting_and_another_without_painting__expect_only_first_artists_in_context(self):
        # create 1st artist and his painting
        user, profile = self._create_valid_user_and_profile()
        self._create_painting(user)
        # create 2nd artists without creating a painting
        other_user, other_profile = self._create_other_user()

        response = self.client.get(reverse('artists'))
        artists_with_paintings_counts = len(response.context['artists'])
        self.assertEqual(1, artists_with_paintings_counts)
        self.assertIn(profile, response.context['artists'])
        self.assertNotIn(other_profile, response.context['artists'])