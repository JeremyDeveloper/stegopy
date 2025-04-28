from stegopy.image import _core
from typing import Optional

def encode(image_path: str, output_path: str, message: str, region: Optional[str] = None, channel: Optional[str] = None, alpha: Optional[bool] = False) -> None:
    """
    Encodes a UTF-8 message into the least significant bits of an image.

    This function wraps the core encoding functionality to provide a simpler interface for encoding messages into images. It supports encoding into specific regions and channels of the image, as well as using the alpha channel.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path where the stego image will be saved.
        message (str): Message to embed.
        region (Optional[str]): Region of the image to embed into. Defaults to None.
        channel (Optional[str]): Specific RGB channel to use. Defaults to None.
        alpha (Optional[bool]): Whether to use the alpha channel. Defaults to False.

    Raises:
        FileNotFoundError: If input image does not exist.
        UnsupportedFormatError: If image cannot be read or is invalid.
        PayloadTooLargeError: If message exceeds capacity.
    """
    _core.encode(image_path, output_path, message, region=region, channel=channel, alpha=alpha)

def decode(image_path: str, region: Optional[str] = None, channel: Optional[str] = None, alpha: Optional[bool] = False) -> str:
    """
    Decodes a UTF-8 message from the least significant bits of an image.

    This function wraps the core decoding functionality to provide a simpler interface for extracting messages from images. It supports decoding from specific regions and channels of the image, as well as from the alpha channel.

    Args:
        image_path (str): Image file containing stego data.
        region (Optional[str]): Region used during encoding. Defaults to None.
        channel (Optional[str]): Channel used during encoding. Defaults to None.
        alpha (Optional[bool]): If message was encoded in alpha channel. Defaults to False.

    Returns:
        str: Decoded message string.

    Raises:
        FileNotFoundError: If file does not exist.
        UnsupportedFormatError: If image format is invalid.
        InvalidStegoDataError: If message is corrupted or incomplete.
    """
    return _core.decode(image_path, region=region, channel=channel, alpha=alpha)
