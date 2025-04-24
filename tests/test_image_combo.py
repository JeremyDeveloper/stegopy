import unittest
import os
from stegopy.image import combo
from stegopy.errors import PayloadTooLargeError, InvalidStegoDataError

TEST_INPUT_IMAGE = "tests/assets/input.png"
TEST_OUTPUT_IMAGE = "tests/assets/output.png"
TEST_MESSAGE = "🧠 combo encoding test"

class TestImageComboStego(unittest.TestCase):

    def test_combo_rgb_center(self):
        combo.encode(TEST_INPUT_IMAGE, TEST_OUTPUT_IMAGE, TEST_MESSAGE, region="center")
        decoded = combo.decode(TEST_OUTPUT_IMAGE, region="center")
        self.assertEqual(decoded, TEST_MESSAGE)

    def test_combo_channel_only(self):
        combo.encode(TEST_INPUT_IMAGE, TEST_OUTPUT_IMAGE, TEST_MESSAGE, channel="g")
        decoded = combo.decode(TEST_OUTPUT_IMAGE, channel="g")
        self.assertEqual(decoded, TEST_MESSAGE)

    def test_combo_alpha_only(self):
        combo.encode(TEST_INPUT_IMAGE, TEST_OUTPUT_IMAGE, TEST_MESSAGE, alpha=True)
        decoded = combo.decode(TEST_OUTPUT_IMAGE, alpha=True)
        self.assertEqual(decoded, TEST_MESSAGE)

    def test_combo_region_and_channel(self):
        combo.encode(TEST_INPUT_IMAGE, TEST_OUTPUT_IMAGE, TEST_MESSAGE, region="topleft", channel="r")
        decoded = combo.decode(TEST_OUTPUT_IMAGE, region="topleft", channel="r")
        self.assertEqual(decoded, TEST_MESSAGE)

    def test_combo_region_and_alpha(self):
        combo.encode(TEST_INPUT_IMAGE, TEST_OUTPUT_IMAGE, TEST_MESSAGE, region="bottomright", alpha=True)
        decoded = combo.decode(TEST_OUTPUT_IMAGE, region="bottomright", alpha=True)
        self.assertEqual(decoded, TEST_MESSAGE)

    def test_payload_too_large(self):
        from PIL import Image
        tiny_path = "tests/assets/tiny.png"
        Image.new("RGB", (1, 1), color=(255, 255, 255)).save(tiny_path)

        with self.assertRaises(PayloadTooLargeError):
            combo.encode(tiny_path, TEST_OUTPUT_IMAGE, "This message is way too long for 1 pixel.", region="topleft", channel="r")

        os.remove(tiny_path)

    def test_invalid_decode(self):
        with open("tests/assets/clean_combo.png", "wb") as f:
            with open(TEST_INPUT_IMAGE, "rb") as input_image:
                f.write(input_image.read())
        with self.assertRaises(InvalidStegoDataError):
            combo.decode("tests/assets/clean_combo.png", region="topleft", channel="r")
        os.remove("tests/assets/clean_combo.png")

    def tearDown(self):
        if os.path.exists(TEST_OUTPUT_IMAGE):
            os.remove(TEST_OUTPUT_IMAGE)

if __name__ == "__main__":
    unittest.main()