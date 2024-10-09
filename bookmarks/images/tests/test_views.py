from http import HTTPStatus

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import django.shortcuts
from django.test import TestCase

from account.models import Profile
from images.models import Images


class TestDetailView(TestCase):
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

    def test_detail_view_valid_data(self):
        self.client.login(username="testuser", password="password")

        url = django.shortcuts.reverse(
            "images:detail",
            kwargs={"id": self.image.id, "slug": self.image.slug},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("image", response.context)
        self.assertEqual(response.context["image"], self.image)
        self.assertEqual(response.context["section"], "images")
        self.assertTemplateUsed(response, "images/image/detail.html")

    def test_detail_view_invalid_data_slug(self):
        self.client.login(username="testuser", password="password")

        url = django.shortcuts.reverse(
            "images:detail",
            kwargs={"id": self.image.id, "slug": "invalid-slug"},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class ImageCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="mail@mail.com",
            password="password",
        )
        self.client.login(username="testuser", password="password")

    def test_create_image_valid_data(self):
        image_file = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg",
        )
        form_data = {
            "title": "Test Image",
            "description": "Test Description",
            "url": "https://example.com/image.jpg",
            "slug": "test-image",
            "image": image_file,
        }

        response = self.client.post(
            django.shortcuts.reverse("images:create"),
            data=form_data,
        )

        self.assertEqual(Images.objects.count(), 1)
        new_image = Images.objects.first()
        self.assertEqual(new_image.title, "Test Image")
        self.assertEqual(new_image.description, "Test Description")
        self.assertEqual(new_image.url, "https://example.com/image.jpg")
        self.assertEqual(new_image.slug, "test-image")

        self.assertRedirects(response, new_image.get_absolute_url())

    def test_create_image_invalid_data(self):
        form_data = {
            "title": "",
            "description": "Test Description",
            "url": "invalid_url",
            "slug": "test-image",
        }

        self.client.post(
            django.shortcuts.reverse("images:create"),
            data=form_data,
        )

        self.assertEqual(Images.objects.count(), 0)
