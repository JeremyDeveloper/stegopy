import mimetypes, os, wave
from typing import List, Optional
from stegopy.errors import InvalidStegoDataError
from PIL import Image

def _is_audio_file(path: str) -> bool:
    """
    Check if a file is an audio file based on MIME type.

    Args:
        path (str): Path to file.

    Returns:
        bool: True if audio, False otherwise.
    """
    mimetype, _ = mimetypes.guess_type(path)
    return mimetype is not None and mimetype.startswith("audio")

def _is_image_file(path: str) -> bool:
    """
    Check if a file is an image file based on MIME type.

    Args:
        path (str): Path to file.

    Returns:
        bool: True if image, False otherwise.
    """
    mimetype, _ = mimetypes.guess_type(path)
    return mimetype is not None and mimetype.startswith("image")

def _int_to_bits(n: int, length: int) -> List[int]:
    """
    Convert an integer into a list of bits of a given length.

    Args:
        n (int): The integer to convert.
        length (int): The number of bits to produce.

    Returns:
        List[int]: A list of 0s and 1s representing the integer.
    """
    return [(n >> i) & 1 for i in range(length - 1, -1, -1)]

def _bits_to_int(bits: List[int]) -> int:
    """
    Convert a list of bits back to an integer.

    Args:
        bits (List[int]): List of 0s and 1s.

    Returns:
        int: The resulting integer.
    """
    return sum(bit << (len(bits) - 1 - i) for i, bit in enumerate(bits))

def _text_to_bits(text: str) -> List[int]:
    """
    Convert a UTF-8 string into a list of bits.

    Args:
        text (str): Input string.

    Returns:
        List[int]: A flat list of bits for each UTF-8 byte.
    """
    return [bit for char in text.encode('utf-8') for bit in _int_to_bits(char, 8)]

def _bits_to_text(bits: List[int]) -> str:
    """
    Convert a list of bits back into a UTF-8 string.

    Args:
        bits (List[int]): Bit list to decode.

    Raises:
        InvalidStegoDataError: If the bits cannot be decoded as UTF-8.

    Returns:
        str: The decoded string.
    """
    chars = []
    for b in range(0, len(bits), 8):
        byte = bits[b:b + 8]
        if len(byte) < 8:
            break
        chars.append(_bits_to_int(byte))
    try:
        return bytes(chars).decode('utf-8')
    except UnicodeDecodeError:
        raise InvalidStegoDataError("Decoded data is not valid UTF-8. Image may not contain stego data.")
    
def _estimate_capacity(path: str, channel: Optional[str] = None, alpha: Optional[bool] = False) -> int:
    """
    Estimate the maximum number of UTF-8 characters that can be embedded in a media file.

    Args:
        path (str): Path to the media file.
        channel (str, optional): Channel used for steganography ('r', 'g', or 'b'). Only for images.
        alpha (bool, optional): Use alpha channel for embedding. Only for images.

    Returns:
        int: Approximate character capacity based on available bits divided by 8.
    """

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    if _is_image_file(path):
        with Image.open(path) as img:
            pixels = list(img.convert("RGBA" if alpha else "RGB").getdata())
            
            if alpha or channel:
                total_bits = len(pixels)
            else:
                total_bits = len(pixels) * 3

            return max(0, (total_bits - 32) // 8)

    if _is_audio_file(path):
        with wave.open(path, 'rb') as audio:
            if audio.getsampwidth() != 2 or audio.getnchannels() != 1:
                raise ValueError("Only 16-bit mono PCM WAV files are supported.")

            frames = audio.getnframes()
            total_bits = frames

            return max(0, (total_bits - 32) // 8)

    return 0
