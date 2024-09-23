from django.test import TestCase

from account.forms import LoginForm


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
