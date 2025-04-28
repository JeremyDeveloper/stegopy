from stegopy.image import _core

def encode(image_path: str, output_path: str, message: str, channel: str = "g") -> None:
    """
    Encodes a UTF-8 message into the least significant bits of a specific color channel of an image.

    This function uses the specified color channel of the image to hide the message.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path where the stego image will be saved.
        message (str): Message to embed.
        channel (str): Specific RGB channel to use. Default is "g".

    Raises:
        FileNotFoundError: If input image does not exist.
        UnsupportedFormatError: If image cannot be read or is invalid.
        PayloadTooLargeError: If message exceeds capacity.
    """
    _core.encode(image_path, output_path, message, channel=channel)

def decode(image_path: str, channel: str = "g") -> str:
    """
    Decodes a UTF-8 message from the least significant bits of a specific color channel of an image.

    This function extracts the message hidden in the specified color channel of the image.

    Args:
        image_path (str): Image file containing stego data.
        channel (str): Channel used during encoding. Default is "g".

    Returns:
        str: Decoded message string.

    Raises:
        FileNotFoundError: If file does not exist.
        UnsupportedFormatError: If image format is invalid.
        InvalidStegoDataError: If message is corrupted or incomplete.
    """
    return _core.decode(image_path, channel=channel)
