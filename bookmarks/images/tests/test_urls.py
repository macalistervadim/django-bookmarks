from http import HTTPStatus

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import django.shortcuts
from django.test import TestCase

from account.models import Profile
from images.models import Images


class TestCreateUrls(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="mail@mail.com",
            password="password",
        )
        self.profile = Profile.objects.create(
            user=self.user,
        )

    def test_create_url_login_user(self):
        self.client.login(username="testuser", password="password")

        request = django.shortcuts.reverse("images:create")
        response = self.client.get(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_url_anonymous_user(self):
        request = django.shortcuts.reverse("images:create")
        response = self.client.get(request)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)


class TestDetailUrls(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="mail@mail.com",
            password="password",
        )
        self.profile = Profile.objects.create(
            user=self.user,
        )

        image_file = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg",
        )
        self.image = Images.objects.create(
            user=self.user,
            title="Test Image",
            description="Test Description",
            url="https://example.com/image.jpg",
            slug="test-image",
            image=image_file,
        )

    def test_detail_url_valid_data(self):
        self.client.login(username="testuser", password="password")

        request = django.shortcuts.reverse(
            "images:detail",
            kwargs={"id": self.image.id, "slug": self.image.slug},
        )
        response = self.client.get(request)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_detail_url_invalid_data(self):
        url = django.shortcuts.reverse(
            "images:detail",
            kwargs={"id": self.image.id, "slug": "invalid-slug"},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
