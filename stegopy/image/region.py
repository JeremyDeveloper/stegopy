from stegopy.image import _core
from typing import Optional

def encode(image_path: str, output_path: str, message: str, region: Optional[str] = "center") -> None:
    """
    Encodes a UTF-8 message into the least significant bits of an image within a specified region.

    This function wraps the core encoding functionality to provide a simpler interface for encoding messages into images. It supports encoding into specific regions of the image.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path where the stego image will be saved.
        message (str): Message to embed.
        region (Optional[str]): Region of the image to embed into. Defaults to "center".

    Raises:
        FileNotFoundError: If input image does not exist.
        UnsupportedFormatError: If image cannot be read or is invalid.
        PayloadTooLargeError: If message exceeds capacity.
    """
    _core.encode(image_path, output_path, message, region=region)

def decode(image_path: str, region: Optional[str] = "center") -> str:
    """
    Decodes a UTF-8 message from the least significant bits of an image within a specified region.

    This function wraps the core decoding functionality to provide a simpler interface for extracting messages from images. It supports decoding from specific regions of the image.

    Args:
        image_path (str): Image file containing stego data.
        region (Optional[str]): Region used during encoding. Defaults to "center".

    Returns:
        str: Decoded message string.

    Raises:
        FileNotFoundError: If file does not exist.
        UnsupportedFormatError: If image format is invalid.
        InvalidStegoDataError: If message is corrupted or incomplete.
    """
    return _core.decode(image_path, region=region)
