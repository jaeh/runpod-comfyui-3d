import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import handler


class TestWorkflowValidation(unittest.TestCase):
    """Tests for workflow input validation."""

    def test_valid_input_with_workflow_only(self):
        input_data = {"workflow": {"key": "value"}}
        validated_data, error = handler.validate_input(input_data)
        self.assertIsNone(error)
        self.assertEqual(validated_data, {"workflow": {"key": "value"}, "images": None})

    def test_valid_input_with_workflow_and_images(self):
        input_data = {
            "workflow": {"key": "value"},
            "images": [{"name": "image1.png", "image": "base64string"}],
        }
        validated_data, error = handler.validate_input(input_data)
        self.assertIsNone(error)
        self.assertEqual(validated_data, input_data)

    def test_input_missing_workflow(self):
        input_data = {"images": [{"name": "image1.png", "image": "base64string"}]}
        validated_data, error = handler.validate_input(input_data)
        self.assertIsNotNone(error)
        self.assertEqual(error, "Missing 'workflow' parameter")

    def test_input_with_invalid_images_structure(self):
        input_data = {
            "workflow": {"key": "value"},
            "images": [{"name": "image1.png"}],
        }
        validated_data, error = handler.validate_input(input_data)
        self.assertIsNotNone(error)
        self.assertEqual(
            error, "'images' must be a list of objects with 'name' and 'image' keys"
        )

    def test_invalid_json_string_input(self):
        input_data = "invalid json"
        validated_data, error = handler.validate_input(input_data)
        self.assertIsNotNone(error)
        self.assertEqual(error, "Invalid JSON format in input")

    def test_valid_json_string_input(self):
        input_data = '{"workflow": {"key": "value"}}'
        validated_data, error = handler.validate_input(input_data)
        self.assertIsNone(error)
        self.assertEqual(validated_data, {"workflow": {"key": "value"}, "images": None})

    def test_empty_input(self):
        input_data = None
        validated_data, error = handler.validate_input(input_data)
        self.assertIsNotNone(error)
        self.assertEqual(error, "Please provide input")


class TestComfyUIHealthCheck(unittest.TestCase):
    """Tests for ComfyUI health check functionality."""

    @patch("handler._session.get")
    def test_comfy_server_status_up(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = handler._comfy_server_status()
        self.assertTrue(result["reachable"])
        self.assertEqual(result["status_code"], 200)

    @patch("handler._session.get")
    def test_comfy_server_status_down(self, mock_get):
        mock_get.side_effect = Exception("Connection refused")

        result = handler._comfy_server_status()
        self.assertFalse(result["reachable"])
        self.assertIn("error", result)

    @patch("handler._session.get")
    def test_check_comfy_healthy_true(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = handler._check_comfy_healthy(force=True)
        self.assertTrue(result)

    @patch("handler._session.get")
    def test_check_comfy_healthy_false(self, mock_get):
        mock_get.side_effect = Exception("Connection refused")

        result = handler._check_comfy_healthy(force=True)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
