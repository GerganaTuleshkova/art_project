from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from art_project.art_portal_app.models import Style, Painting
from art_project.mixins import ArrangeMixin

UserModel = get_user_model()


class PaintingsViewTests(ArrangeMixin, TestCase):

    def test__expect_correct_template_used(self):
        response = self.client.get(reverse('all paintings'))
        self.assertTemplateUsed(response, 'art_portal_templates/paintings.html')

    def test_with_no_paintings__expect_no_paintings_in_context(self):
        response = self.client.get(reverse('all paintings'))
        paintings_counts = len(response.context['paintings'])
        self.assertEqual(0, paintings_counts)

    def test_with_2_paintings__expect_2_paintings_in_context(self):
        # create 1st artist and his painting
        user, profile = self._create_valid_user_and_profile()
        painting1 = self._create_painting(user)
        # create 2nd artists and his painting
        other_user, other_profile = self._create_other_user()
        painting2 = self._create_painting(other_user)

        response = self.client.get(reverse('all paintings'))
        paintings_counts = len(response.context['paintings'])
        self.assertEqual(2, paintings_counts)
        self.assertIn(painting1, response.context['paintings'])
        self.assertIn(painting2, response.context['paintings'])

    def test_filter_on_style_with_1_painting_in_the_style__expect_one_painting_in_context(self):
        # create 1st artist and his painting
        user, profile = self._create_valid_user_and_profile()
        painting1 = self._create_painting(user)

        response = self.client.get(reverse('all paintings')+'?q=Impressionism')
        paintings_counts = len(response.context['paintings'])
        self.assertEqual(1, paintings_counts)
        self.assertIn(painting1, response.context['paintings'])

    def test_filter_on_style_with_1_painting_not_in_the_style__expect_no_painting_in_context(self):
        # create 1st artist and his painting
        user, profile = self._create_valid_user_and_profile()
        painting1 = self._create_painting(user)

        response = self.client.get(reverse('all paintings')+'?q=Cubism')
        paintings_counts = len(response.context['paintings'])
        self.assertEqual(0, paintings_counts)
        self.assertNotIn(painting1, response.context['paintings'])

    def test_pagination_with_7_paintings__expect_2_pages(self):
        user, profile = self._create_valid_user_and_profile()
        for _ in range(7):
            self._create_painting(user)

        response = self.client.get(reverse('all paintings')+'?page=2')
        check = response.context['paintings']
        self.assertEquals(2, response.context_data['page_obj'].number)

