from django.test import TestCase

import images.forms


class ImageFormTests(TestCase):
    def test_image_form_valid_data(self):
        form_data = {
            "title": "test",
            "url": "https://test.com/image.png",
        }
        form = images.forms.ImagesCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_image_form_invalid_data(self):
        form_data = {
            "title": "",
            "url": "test",
        }
        form = images.forms.ImagesCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["title"], ["This field is required."])
        self.assertEqual(form.errors["url"], ["Enter a valid URL."])

    def test_image_form_invalid_url(self):
        form_data = {
            "title": "test",
            "url": "https://test.com/image.gif",
        }
        form = images.forms.ImagesCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["url"],
            ["The given URL doest not match valid image extensions."],
        )
