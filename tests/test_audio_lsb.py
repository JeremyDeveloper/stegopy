import unittest, os
from stegopy.audio import lsb
from stegopy.errors import (
    PayloadTooLargeError,
    InvalidStegoDataError
)

TEST_INPUT_WAV = "tests/assets/input.wav"
TEST_OUTPUT_WAV = "tests/assets/output.wav"
TEST_MESSAGE = "Audio stego is alive 🧠"

class TestAudioLSB(unittest.TestCase):
    def test_encode_and_decode(self):
        lsb.encode(TEST_INPUT_WAV, TEST_OUTPUT_WAV, TEST_MESSAGE)
        decoded = lsb.decode(TEST_OUTPUT_WAV)
        self.assertEqual(decoded, TEST_MESSAGE)

    def test_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            lsb.encode("no.wav", TEST_OUTPUT_WAV, TEST_MESSAGE)

    def test_payload_too_large(self):
        import wave
        import struct
        tiny_path = "tests/assets/tiny.wav"
        with wave.open(tiny_path, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(44100)
            samples = [0] * 16
            wf.writeframes(b''.join(struct.pack('<h', s) for s in samples))

        with self.assertRaises(PayloadTooLargeError):
            lsb.encode(tiny_path, TEST_OUTPUT_WAV, "Too big")

        os.remove(tiny_path)

    def test_invalid_stego_data(self):
        import wave
        import struct
        clean_path = "tests/assets/clean.wav"
        with wave.open(clean_path, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(44100)
            wf.writeframes(b''.join(struct.pack('<h', 0) for _ in range(1000)))

        with self.assertRaises(InvalidStegoDataError):
            lsb.decode(clean_path)

        os.remove(clean_path)

    def tearDown(self):
        if os.path.exists(TEST_OUTPUT_WAV):
            os.remove(TEST_OUTPUT_WAV)

if __name__ == "__main__":
    unittest.main()