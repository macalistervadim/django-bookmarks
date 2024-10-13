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


class TestImageLikeUrls(TestCase):
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

    def test_image_like_url_valid(self):
        self.client.login(username="testuser", password="password")
        url = django.shortcuts.reverse("images:like")

        response = self.client.post(
            url,
            {"id": self.image.id, "action": "like"},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertJSONEqual(response.content, {"status": "ok"})

    def test_image_unlike_url_valid(self):
        self.client.login(username="testuser", password="password")
        self.image.users_like.add(self.user)
        url = django.shortcuts.reverse("images:like")

        response = self.client.post(
            url,
            {"id": self.image.id, "action": "unlike"},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertJSONEqual(response.content, {"status": "ok"})


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


class TestImageListUrls(TestCase):
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

    def test_image_list_url_valid(self):
        self.client.login(username="testuser", password="password")

        url = django.shortcuts.reverse("images:list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Test Image")

    def test_image_list_url_anonymous_user(self):
        url = django.shortcuts.reverse("images:list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        url_redirect = (
            django.shortcuts.reverse("account:login") + "?next=" + url
        )
        self.assertRedirects(response, url_redirect)
