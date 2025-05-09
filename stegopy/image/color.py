from stegopy.image import _core

def encode(image_path: str, output_path: str, payload: str, channel: str = "g") -> None:
    """
    Encodes a payload into the least significant bits of a specific color channel of an image.

    This function uses the specified color channel of the image to hide the payload.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path where the stego image will be saved.
        payload (str): Payload to embed.
        channel (str): Specific RGB channel to use. Default is "g".

    Raises:
        FileNotFoundError: If input image does not exist.
        UnsupportedFormatError: If image cannot be read or is invalid.
        PayloadTooLargeError: If payload exceeds capacity.
    """
    _core.encode(image_path, output_path, payload, channel=channel)

def decode(image_path: str, channel: str = "g") -> str:
    """
    Decodes a payload from the least significant bits of a specific color channel of an image.

    This function extracts the payload hidden in the specified color channel of the image.

    Args:
        image_path (str): Image file containing stego data.
        channel (str): Channel used during encoding. Default is "g".

    Returns:
        str: The decoded payload..

    Raises:
        FileNotFoundError: If file does not exist.
        UnsupportedFormatError: If image format is invalid.
        InvalidStegoDataError: If payload is corrupted or incomplete.
    """
    return _core.decode(image_path, channel=channel)
