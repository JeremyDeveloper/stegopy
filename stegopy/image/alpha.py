from stegopy.image import _core

def encode(image_path: str, output_path: str, payload: str) -> None:
    """
    Encodes a payload into the alpha channel of an image.

    This function uses the alpha channel of the image to hide the payload.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path where the stego image will be saved.
        payload (str): Payload to embed.

    Raises:
        FileNotFoundError: If input image does not exist.
        UnsupportedFormatError: If image cannot be read or is invalid.
        PayloadTooLargeError: If payload exceeds capacity.
    """
    _core.encode(image_path, output_path, payload, alpha=True)

def decode(image_path: str) -> str:
    """
    Decodes a payload from the alpha channel of an image.

    This function extracts the payload hidden in the alpha channel of the image.

    Args:
        image_path (str): Image file containing stego data.

    Returns:
        str: The decoded payload..

    Raises:
        FileNotFoundError: If file does not exist.
        UnsupportedFormatError: If image format is invalid.
        InvalidStegoDataError: If payload is corrupted or incomplete.
    """
    return _core.decode(image_path, alpha=True)
    