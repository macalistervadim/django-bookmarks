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
    def test_user_login_url(self):
        response = self.client.get(reverse("account:login"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
