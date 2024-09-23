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
