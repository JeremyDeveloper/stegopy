import unittest
from stegopy.utils import (
    _int_to_bits,
    _bits_to_int,
    _text_to_bits,
    _bits_to_text,
    _estimate_capacity
)
from stegopy.errors import InvalidStegoDataError

class TestUtils(unittest.TestCase):
    def test_int_to_bits_and_back(self):
        original = 12345
        bits = _int_to_bits(original, 16)
        reconstructed = _bits_to_int(bits)
        self.assertEqual(original, reconstructed)

    def test_text_to_bits_and_back_ascii(self):
        original = "hello"
        bits = _text_to_bits(original)
        result = _bits_to_text(bits)
        self.assertEqual(original, result)

    def test_text_to_bits_and_back_emoji(self):
        original = "brain 🧠 power"
        bits = _text_to_bits(original)
        result = _bits_to_text(bits)
        self.assertEqual(original, result)

    def test_invalid_utf8_triggers_error(self):
        bad_bits = [1] * 32
        with self.assertRaises(InvalidStegoDataError):
            _bits_to_text(bad_bits)

    def test_estimate_capacity_image_rgb(self):
        cap = _estimate_capacity("tests/assets/input.png")
        self.assertTrue(cap > 0)

    def test_estimate_capacity_image_alpha(self):
        cap = _estimate_capacity("tests/assets/input.png", alpha=True)
        self.assertTrue(cap > 0)

    def test_estimate_capacity_image_channel(self):
        cap = _estimate_capacity("tests/assets/input.png", channel='g')
        self.assertTrue(cap > 0)

    def test_estimate_capacity_audio(self):
        cap = _estimate_capacity("tests/assets/input.wav")
        self.assertTrue(cap > 0)

if __name__ == "__main__":
    unittest.main()
