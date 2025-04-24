import os
import unittest
from stegopy.image import region
from stegopy.errors import PayloadTooLargeError, InvalidStegoDataError

TEST_INPUT_IMAGE = "tests/assets/input.png"
TEST_OUTPUT_IMAGE = "tests/assets/output.png"
TEST_MESSAGE = "Hidden with autistic region precision 🧠"

class TestImageRegionStego(unittest.TestCase):
    def test_region_center(self):
        region.encode(TEST_INPUT_IMAGE, TEST_OUTPUT_IMAGE, TEST_MESSAGE, region="center")
        decoded = region.decode(TEST_OUTPUT_IMAGE, region="center")
        self.assertEqual(decoded, TEST_MESSAGE)

    def test_region_topleft(self):
        region.encode(TEST_INPUT_IMAGE, TEST_OUTPUT_IMAGE, TEST_MESSAGE, region="topleft")
        decoded = region.decode(TEST_OUTPUT_IMAGE, region="topleft")
        self.assertEqual(decoded, TEST_MESSAGE)

    def test_region_topright(self):
        region.encode(TEST_INPUT_IMAGE, TEST_OUTPUT_IMAGE, TEST_MESSAGE, region="topright")
        decoded = region.decode(TEST_OUTPUT_IMAGE, region="topright")
        self.assertEqual(decoded, TEST_MESSAGE)

    def test_region_bottomleft(self):
        region.encode(TEST_INPUT_IMAGE, TEST_OUTPUT_IMAGE, TEST_MESSAGE, region="bottomleft")
        decoded = region.decode(TEST_OUTPUT_IMAGE, region="bottomleft")
        self.assertEqual(decoded, TEST_MESSAGE)

    def test_region_bottomright(self):
        region.encode(TEST_INPUT_IMAGE, TEST_OUTPUT_IMAGE, TEST_MESSAGE, region="bottomright")
        decoded = region.decode(TEST_OUTPUT_IMAGE, region="bottomright")
        self.assertEqual(decoded, TEST_MESSAGE)

    def test_payload_too_large(self):
        from PIL import Image
        tiny_path = "tests/assets/tiny.png"
        Image.new("RGB", (1, 1), color=(255, 255, 255)).save(tiny_path)

        with self.assertRaises(PayloadTooLargeError):
            region.encode(tiny_path, TEST_OUTPUT_IMAGE, "This message is way too long for 1 pixel.")

        os.remove(tiny_path)

    def test_invalid_region(self):
        with self.assertRaises(ValueError):
            region.encode(TEST_INPUT_IMAGE, TEST_OUTPUT_IMAGE, TEST_MESSAGE, region="unknown")

    def tearDown(self):
        if os.path.exists(TEST_OUTPUT_IMAGE):
            os.remove(TEST_OUTPUT_IMAGE)