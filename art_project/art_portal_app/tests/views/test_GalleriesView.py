from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from art_project.mixins import ArrangeMixin

UserModel = get_user_model()


class GalleriesViewTests(ArrangeMixin, TestCase):

    def test__expect_correct_template_used(self):
        response = self.client.get(reverse('galleries'))
        self.assertTemplateUsed(response, 'art_portal_templates/galleries.html')

    def test_when_no_galleries__expect_galleries_count_is_0(self):
        response = self.client.get(reverse('galleries'))
        galleries_counts = len(response.context['galleries'])

        self.assertEqual(0, galleries_counts)

    def test_when_1_gallery__expect_galleries_count_is_1(self):
        self._create_gallery()
        response = self.client.get(reverse('galleries'))
        galleries_counts = len(response.context['galleries'])

        self.assertEqual(1, galleries_counts)

    def test_when_1_gallery__expect_gallery_in_list(self):
        gallery_made = self._create_gallery()
        response = self.client.get(reverse('galleries'))

        galleries = response.context['galleries']

        self.assertIn(gallery_made, galleries)
        self.assertEqual(gallery_made, galleries[0])