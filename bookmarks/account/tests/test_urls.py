from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestDashboardUrls(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            password="testpassword",
        )

    def test_dashboard_url_anonumoys(self):
        request = reverse("account:dashboard")
        response = self.client.get(request)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn(reverse("account:login"), response.url)

    def test_dashboard_url_login(self):
        self.client.login(username="user1", password="testpassword")

        request = reverse("account:dashboard")
        response = self.client.get(request)

        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestUserLoginUrls(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            password="testpassword",
        )

    def test_user_login_url_login_user(self):
        self.client.login(username="user1", password="testpassword")

        response = self.client.get(reverse("account:login"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_login_url_anonymous_user(self):
        response = self.client.get(reverse("account:login"))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestPasswordChangeUrls(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            password="testpass",
        )

    def test_password_change_url_login(self):
        self.client.login(username="user1", password="testpass")

        response = self.client.get(reverse("account:password_change"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_password_change_url_anonymous(self):
        response = self.client.get(reverse("account:password_change"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_password_change_done_url_login(self):
        self.client.login(username="user1", password="testpass")

        response = self.client.get(reverse("account:password_change_done"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_password_change_done_url_anonymous(self):
        response = self.client.get(reverse("account:password_change_done"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
