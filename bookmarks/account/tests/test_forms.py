from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.test import TestCase

from account.forms import LoginForm, UserRegistrationForm


class TestLoginForm(TestCase):
    def test_login_form_valid_data(self):
        form_data = {"username": "user1", "password": "testpassword"}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid_data(self):
        form_data = {"username": "", "password": ""}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password", form.errors)


class TestPasswordChangeForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="old_password",
        )

    def test_change_password_form_valid_data(self):
        form_data = {
            "old_password": "old_password",
            "new_password1": "new_password",
            "new_password2": "new_password",
        }
        form = PasswordChangeForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_change_password_form_invalid_data(self):
        form_data = {
            "old_password": "old_password",
            "new_password1": "new_pass",
            "new_password2": "new_password",
        }
        form = PasswordChangeForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())

        self.assertIn("new_password2", form.errors)


class TestUserRegistrationForm(TestCase):
    def test_user_registration_form(self):
        form_data = {
            "username": "testuser",
            "email": "mail@mail.com",
            "first_name": "Test",
            "password": "password1",
            "password2": "password1",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_registration_form_invalid(self):
        form_data = {
            "username": "testuser",
            "email": "mail@mail.com",
            "first_name": "Test",
            "password": "password1",
            "password2": "password1231231",
        }
        form = UserRegistrationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)
