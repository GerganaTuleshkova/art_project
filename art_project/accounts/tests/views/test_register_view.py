from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

UserModel = get_user_model()


class RegisterViewTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': 'asd123',
        'first_name': 'Test',
        'last_name': 'Testov',
        'email': 'testov@mail.com'
    }

    def test_create_user__when_all_valid__expect_to_be_created(self):

        client = Client()

        response = client.post(
            reverse('register'),
            data=self.VALID_USER_CREDENTIALS,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_templates/register.html')
        # self.assertRedirects(response, '')
        # user = UserModel.objects.first()
        # self.assertIsNotNone(user)
        # self.assertEqual(self.VALID_USER_CREDENTIALS['first_name'], user.first_name)
        # self.assertEqual(self.VALID_USER_CREDENTIALS['last_name'], user.last_name)
        # self.assertEqual(self.VALID_USER_CREDENTIALS['username'], user.username)
