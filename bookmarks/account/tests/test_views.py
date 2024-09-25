from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestDashboardView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            password="testpassword",
        )

    def test_dashboard_view(self):
        self.client.login(username="user1", password="testpassword")

        response = self.client.get(reverse("account:dashboard"))
        self.assertTemplateUsed(response, "account/dashboard.html")

        self.assertIn("section", response.context)
        self.assertEqual(response.context["section"], "dashboard")


class TestLoginUserView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            password="testpassword",
        )

        self.inactive_user = User.objects.create_user(
            username="inactive_user",
            password="testpassword",
        )
        self.inactive_user.is_active = False
        self.inactive_user.save()

    def test_get_login_user_view(self):
        response = self.client.get(reverse("account:login"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_post_login_user_valid_data(self):
        response = self.client.post(
            reverse("account:login"),
            {"username": "user1", "password": "testpassword"},
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("account:dashboard"))

    def test_post_login_inactive_user(self):
        response = self.client.post(
            reverse("account:login"),
            {"username": "inactive_user", "password": "testpassword"},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_login_user_invalid_data(self):
        response = self.client.post(
            reverse("account:login"),
            {"username": "user1", "password": "wrongpassword"},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_login_empty_data(self):
        response = self.client.post(
            reverse("account:login"),
            {"username": "", "password": ""},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestPasswordChange(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="old_password",
        )
        self.client.login(username="testuser", password="old_password")

    def test_password_change_view(self):
        response = self.client.get(reverse("account:password_change"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(
            response,
            "registration/password_change_form.html",
        )

    def test_successful_password_change(self):
        response = self.client.post(
            reverse("account:password_change"),
            {
                "old_password": "old_password",
                "new_password1": "new_password",
                "new_password2": "new_password",
            },
        )
        self.assertRedirects(response, reverse("account:password_change_done"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("new_password"))

    def test_unsuccessful_password_change_with_incorrect_old_password(self):
        response = self.client.post(
            reverse("account:password_change"),
            {
                "old_password": "wrong_password",
                "new_password1": "new_password",
                "new_password2": "new_password",
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(
            response,
            "registration/password_change_form.html",
        )

        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn(
            "Your old password was entered incorrectly. "
            "Please enter it again.",
            form.errors["old_password"],
        )
