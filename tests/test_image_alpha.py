import unittest
import os
from stegopy.image import alpha
from stegopy.errors import PayloadTooLargeError, InvalidStegoDataError

TEST_INPUT_IMAGE = "tests/assets/input.png"
TEST_OUTPUT_IMAGE = "tests/assets/output_alpha.png"
TEST_MESSAGE = "🧠 Alpha Stego Works 🦕"

class TestImageAlphaStego(unittest.TestCase):
    def test_encode_and_decode(self):
        alpha.encode(TEST_INPUT_IMAGE, TEST_OUTPUT_IMAGE, TEST_MESSAGE)
        decoded = alpha.decode(TEST_OUTPUT_IMAGE)
        self.assertEqual(decoded, TEST_MESSAGE)

    def test_payload_too_large(self):
        from PIL import Image
        small_path = "tests/assets/tiny_color.png"
        Image.new("RGB", (1, 1), color=(255, 255, 255)).save(small_path)

        with self.assertRaises(PayloadTooLargeError):
            alpha.encode(small_path, TEST_OUTPUT_IMAGE, "🚂")

    def test_invalid_decode(self):
        clean_output = "tests/assets/clean_output.png"
        from PIL import Image
        Image.new("RGBA", (100, 100), (0, 0, 0, 255)).save(clean_output)

        with self.assertRaises(InvalidStegoDataError):
            alpha.decode(clean_output)

        os.remove(clean_output)

    def tearDown(self):
        if os.path.exists(TEST_OUTPUT_IMAGE):
            os.remove(TEST_OUTPUT_IMAGE)

if __name__ == "__main__":
    unittest.main()
