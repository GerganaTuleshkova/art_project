from django.test import TestCase

from art_project.accounts.forms import UserUpdateForm


class UserUpdateFormTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test.user@mail.com'
    }

    def test_with_valid_data__expect_valid_form(self):
        form = UserUpdateForm(data=self.VALID_USER_CREDENTIALS)
        self.assertTrue(form.is_valid())

    def test_with_invalid_email__expect_invalid_form(self):
        invalid_user_credentials = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user'
        }
        form = UserUpdateForm(data=invalid_user_credentials)
        self.assertFalse(form.is_valid())

