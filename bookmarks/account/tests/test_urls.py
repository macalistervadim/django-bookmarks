from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from account.models import Profile


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


class TestPasswordResetUrls(TestCase):
    def test_password_reset_url(self):
        response = self.client.get(reverse("account:password_reset"))
        self.assertEqual(response.status_code, HTTPStatus.OK)


class TestEditProfileUrls(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="mail@mail.com",
            password="password",
        )
        self.profile = Profile.objects.create(user=self.user)

    def test_edit_profile_url(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("account:edit"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_profile_anonymous(self):
        response = self.client.get(reverse("account:edit"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


class TestRegistrationUserUrls(TestCase):
    def test_registration_url(self):
        response = self.client.get(reverse("account:register"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_registration_url_successfully_register(self):
        data = {
            "username": "user1",
            "first_name": "John",
            "email": "mail@mail.ru",
            "password": "password",
            "password2": "password",
        }

        self.client.post(reverse("account:register"), data)

        user = User.objects.get(username="user1")
        self.assertIsNotNone(user)


class TestUserFollowUrls(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="mail@mail.com",
            password="password",
        )

    def test_user_follow_url_login_user_get_method(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("account:user_follow"))

        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_user_follow_url_anonymous_user(self):
        response = self.client.get(reverse("account:user_follow"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        url_redirect = (
            reverse("account:login")
            + "?next="
            + reverse("account:user_follow")
        )
        self.assertRedirects(response, url_redirect)
