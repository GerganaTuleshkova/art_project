from django.test import TestCase

from art_project.accounts.forms import ProfileUpdateForm


class ProfileUpdateFormTests(TestCase):
    PROFILE_VALID_DATA = {
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test.user@mail.com',
        'facebook link': 'https://testov.com',
    }

    def test_all_valid_data__expect_valid_form(self):
        form = ProfileUpdateForm(data=self.PROFILE_VALID_DATA)
        self.assertTrue(form.is_valid())

    def test_with_invalid_phone_number__expect_invalid_form(self):
        invalid_profile_data = {
            'phone_number': 'abc',
        }
        form = ProfileUpdateForm(data=invalid_profile_data)

        self.assertFalse(form.is_valid())
