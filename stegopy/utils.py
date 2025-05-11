import mimetypes, contextlib, io, os, wave, aifc
from typing import List, Optional
from stegopy.errors import InvalidStegoDataError, UnsupportedFormatError
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
    if path.lower().endswith(".webp"):
        return True
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

def _image_to_bits(img: Image.Image) -> List[int]:
    """
    Convert a PIL image to a flat list of bits representing the image file.

    The image is serialized in-memory using lossless PNG format, then each byte
    of the file is converted to its 8-bit binary representation.

    Args:
        img (Image.Image): PIL Image object to convert.

    Returns:
        List[int]: A flat list of bits (0s and 1s) representing the serialized image.
    """
    with io.BytesIO() as buffer:
        img.save(buffer, format="PNG")
        raw_bytes = buffer.getvalue()
    return [bit for byte in raw_bytes for bit in _int_to_bits(byte, 8)]

def _bits_to_image(bits: List[int]) -> Image.Image:
    """
    Convert a list of bits back into a PIL Image.

    This reconstructs a valid image from raw bit data by grouping every 8 bits into bytes,
    reassembling the full byte stream, and loading it into a PIL Image via an in-memory buffer.

    Args:
        bits (List[int]): Bit list representing an encoded image (must be valid image bytes).

    Returns:
        Image.Image: PIL Image reconstructed from the input bitstream.

    Raises:
        UnidentifiedImageError: If the resulting byte stream is not a valid image format.
    """
    byte_data = bytes([_bits_to_int(bits[i:i+8]) for i in range(0, len(bits), 8)])
    return Image.open(io.BytesIO(byte_data))

def _open_audio(path: str, mode: str) -> contextlib.closing:
    """
    Opens a WAV or AIFF file in read or write mode.

    Args:
        path (str): Path to the audio file (.wav, .aif, or .aiff).
        mode (str): Mode to open the file in ('rb' or 'wb').

    Returns:
        contextlib.closing: Context manager with the opened wave/aifc stream.
    """
    if path.lower().endswith(".aiff") or path.lower().endswith(".aif"):
        return contextlib.closing(aifc.open(path, mode))
    return contextlib.closing(wave.open(path, mode))

def _estimate_capacity(path: str, region: Optional[str] = None, channel: Optional[str] = None, alpha: bool = False) -> int:
    """
    Estimate the number of UTF-8 characters that can be hidden in the file.

    Args:
        path (str): Path to the image or audio file.
        region (Optional[str]): Region to encode into (if any, for images).
        channel (Optional[str]): Channel to encode into (if any, for images).
        alpha (Optional[bool]): Whether alpha channel is used (for images).

    Returns:
        int: Estimated number of UTF-8 characters that can be embedded.

    Raises:
        FileNotFoundError: If the file does not exist.
        UnsupportedFormatError: If the file is not a supported type.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    if _is_audio_file(path):
        with _open_audio(path, 'rb') as audio:
            params = audio.getparams()
            if params.sampwidth != 2 or params.nchannels != 1:
                raise UnsupportedFormatError("Only 16-bit mono PCM audio is supported.")
            bits = len(audio.readframes(audio.getnframes())) * 8 // 16
            return (bits - 40) // 8

    if _is_image_file(path):
        img = Image.open(path)
        img = img.convert("RGBA" if alpha else "RGB")
        width, height = img.size

        if region:
            x_half = width // 2
            y_half = height // 2
            if region == "center":
                region_size = x_half * y_half
            else:
                region_size = x_half * y_half
        else:
            region_size = width * height

        if alpha:
            bits = region_size
        elif channel:
            bits = region_size
        else:
            bits = region_size * 3

        return (bits - 40) // 8

    raise UnsupportedFormatError("Only image and audio files are supported.")
