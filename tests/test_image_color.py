import unittest, os
from stegopy.image import color as color_channel
from stegopy.errors import (
    PayloadTooLargeError,
    InvalidStegoDataError,
)

TEST_INPUT_IMAGE = "tests/assets/input.png"
TEST_OUTPUT_IMAGE = "tests/assets/output.png"
TEST_MESSAGE = "Color channel test!"

class TestColorChannelStego(unittest.TestCase):
    def test_encode_and_decode_blue_channel(self):
        color_channel.encode(TEST_INPUT_IMAGE, TEST_OUTPUT_IMAGE, TEST_MESSAGE, channel='b')
        decoded = color_channel.decode(TEST_OUTPUT_IMAGE, channel='b')
        self.assertEqual(decoded, TEST_MESSAGE)

    def test_encode_and_decode_red_channel(self):
        color_channel.encode(TEST_INPUT_IMAGE, TEST_OUTPUT_IMAGE, TEST_MESSAGE, channel='r')
        decoded = color_channel.decode(TEST_OUTPUT_IMAGE, channel='r')
        self.assertEqual(decoded, TEST_MESSAGE)

    def test_encode_and_decode_green_channel(self):
        color_channel.encode(TEST_INPUT_IMAGE, TEST_OUTPUT_IMAGE, TEST_MESSAGE, channel='g')
        decoded = color_channel.decode(TEST_OUTPUT_IMAGE, channel='g')
        self.assertEqual(decoded, TEST_MESSAGE)

    def test_invalid_channel(self):
        with self.assertRaises(ValueError):
            color_channel.encode(TEST_INPUT_IMAGE, TEST_OUTPUT_IMAGE, TEST_MESSAGE, channel='x')

    def test_payload_too_large(self):
        from PIL import Image
        small_path = "tests/assets/tiny_color.png"
        Image.new("RGB", (1, 1), color=(255, 255, 255)).save(small_path)

        with self.assertRaises(PayloadTooLargeError):
            color_channel.encode(small_path, TEST_OUTPUT_IMAGE, "Way too big", channel='g')

        os.remove(small_path)

    def test_invalid_stego_data(self):
        from PIL import Image
        clean_path = "tests/assets/clean_model.png"
        img = Image.new("RGB", (100, 100), color=(255, 255, 255))  # all-white
        img.save(clean_path)

        with self.assertRaises(InvalidStegoDataError):
            color_channel.decode(clean_path, channel="g")

        os.remove(clean_path)

    def tearDown(self):
        if os.path.exists(TEST_OUTPUT_IMAGE):
            os.remove(TEST_OUTPUT_IMAGE)

if __name__ == "__main__":
    unittest.main()
