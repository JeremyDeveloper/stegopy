import unittest, os
from stegopy.image import lsb
from stegopy.errors import (
    UnsupportedFormatError,
    PayloadTooLargeError,
    InvalidStegoDataError,
)

TEST_INPUT_IMAGE = "tests/assets/input.png"
TEST_OUTPUT_IMAGE = "tests/assets/output.png"
TEST_MESSAGE = "Secret from Jeremiah 🧠"

class TestImageLSB(unittest.TestCase):
    def test_encode_and_decode_message(self):
        lsb.encode(TEST_INPUT_IMAGE, TEST_OUTPUT_IMAGE, TEST_MESSAGE)
        decoded = lsb.decode(TEST_OUTPUT_IMAGE)
        self.assertEqual(decoded, TEST_MESSAGE)

    def test_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            lsb.encode("nonexistent.png", TEST_OUTPUT_IMAGE, TEST_MESSAGE)

    def test_invalid_image(self):
        invalid_path = "tests/assets/not_an_image.txt"
        with open(invalid_path, "w") as f:
            f.write("not an image")
        with self.assertRaises(UnsupportedFormatError):
            lsb.encode(invalid_path, TEST_OUTPUT_IMAGE, TEST_MESSAGE)

    def test_payload_too_large(self):
        from PIL import Image
        tiny_path = "tests/assets/tiny.png"
        Image.new("RGB", (1, 1), color=(255, 255, 255)).save(tiny_path)

        with self.assertRaises(PayloadTooLargeError):
            lsb.encode(tiny_path, TEST_OUTPUT_IMAGE, "This message is way too long for 1 pixel.")

        os.remove(tiny_path)

    def test_invalid_stego_data(self):
        clean_path = "tests/assets/clean.png"
        from PIL import Image
        Image.new("RGB", (10, 10), color=(123, 123, 123)).save(clean_path)

        with self.assertRaises(InvalidStegoDataError):
            lsb.decode(clean_path)

        os.remove(clean_path)

    def tearDown(self):
        if os.path.exists(TEST_OUTPUT_IMAGE):
            os.remove(TEST_OUTPUT_IMAGE)
        if os.path.exists("tests/assets/not_an_image.txt"):
            os.remove("tests/assets/not_an_image.txt")

if __name__ == "__main__":
    unittest.main()
