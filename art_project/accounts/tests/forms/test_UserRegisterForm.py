from django.test import TestCase

from art_project.accounts.forms import UserRegisterForm


class UserRegisterFormTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password1': 'asd123hrjstl&^',
        'password2': 'asd123hrjstl&^',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test.user@mail.com'
    }

    def test_with_all_valid_data__expect_valid_form(self):
        form = UserRegisterForm(data=self.VALID_USER_CREDENTIALS)
        self.assertTrue(form.is_valid())

    def test_with_nonmatching_passwords__expect_invalid_form(self):
        invalid_user_credentials = {
            'username': 'testuser',
            'password1': 'asd',
            'password2': 'asd123hrjstl&^',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test.user@mail.com'
        }
        form = UserRegisterForm(data=invalid_user_credentials)
        self.assertFalse(form.is_valid())

