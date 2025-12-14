import os
from unittest.mock import patch

from django.test import SimpleTestCase
from django.urls import reverse


class AskViewTests(SimpleTestCase):
    def test_get_renders_form(self):
        response = self.client.get(reverse("assistant:ask"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ask ChatGPT")

    def test_missing_api_key_shows_error(self):
        response = self.client.post(reverse("assistant:ask"), {"question": "Hi"})
        self.assertContains(response, "OpenAI API key is not configured")

    def test_successful_post_calls_api(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False):
            with patch("assistant.views._call_chatgpt", return_value="Hello!") as mock_call:
                response = self.client.post(reverse("assistant:ask"), {"question": "Ping"})
        mock_call.assert_called_once()
        self.assertContains(response, "Hello!")
