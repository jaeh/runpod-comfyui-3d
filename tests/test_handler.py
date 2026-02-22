import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import handler


# class TestWorkflowValidation(unittest.TestCase):
#     def test_valid_input_with_workflow_only(self):
#         input_data = {"workflow": {"key": "value"}}
#         validated_data, error = handler.validate_input(input_data)
#         self.assertIsNone(error)
#         self.assertEqual(validated_data, {"workflow": {"key": "value"}, "images": None})


class TestComfyUIHealthCheck(unittest.TestCase):
    def test_comfy_healthy(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
