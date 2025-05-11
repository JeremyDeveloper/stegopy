from stegopy.image import _core
from typing import Optional

def encode(image_path: str, output_path: str, payload: str, region: Optional[str] = "center", frame: Optional[int] = None) -> None:
    """
    Encodes a payload into the least significant bits of an image within a specified region.

    This function wraps the core encoding functionality to provide a simpler interface for encoding payloads into images. It supports encoding into specific regions of the image.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path where the stego image will be saved.
        payload (str): Payload to embed.
        region (Optional[str]): Region of the image to embed into. Defaults to "center".
        frame (Optional[int]): Target frame index for animated images (e.g. GIF).

    Raises:
        FileNotFoundError: If input image does not exist.
        UnsupportedFormatError: If image cannot be read or is invalid.
        PayloadTooLargeError: If payload exceeds capacity.
    """
    _core.encode(image_path, output_path, payload, region=region, frame=frame)

def decode(image_path: str, region: Optional[str] = "center", frame: Optional[int] = None) -> str:
    """
    Decodes a payload from the least significant bits of an image within a specified region.

    This function wraps the core decoding functionality to provide a simpler interface for extracting payloads from images. It supports decoding from specific regions of the image.

    Args:
        image_path (str): Image file containing stego data.
        region (Optional[str]): Region used during encoding. Defaults to "center".
        frame (Optional[int]): Target frame index for animated images (e.g. GIF).
        
    Returns:
        str: The decoded payload.

    Raises:
        FileNotFoundError: If file does not exist.
        UnsupportedFormatError: If image format is invalid.
        InvalidStegoDataError: If payload is corrupted or incomplete.
    """
    return _core.decode(image_path, region=region, frame=frame)
