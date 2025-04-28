from stegopy.audio import _core

def encode(input_path: str, output_path: str, message: str) -> None:
    """
    Encodes a UTF-8 message into the least significant bits of each 16-bit sample in a mono WAV or AIFF file.

    This function utilizes lossless audio bit manipulation to directly embed the message within the sample data. The message is prefixed with a 32-bit integer representing its length, ensuring accurate decoding.

    Args:
        input_path (str): Path to the input WAV or AIFF file.
        output_path (str): Output path for the stego audio file.
        message (str): UTF-8 string to embed.

    Raises:
        FileNotFoundError: If the audio file does not exist.
        UnsupportedFormatError: If the file is not 16-bit mono PCM.
        PayloadTooLargeError: If the message exceeds available LSB capacity.
    """
    _core.encode(input_path, output_path, message)

def decode(input_path: str) -> str:
    """
    Decodes a UTF-8 message from the least significant bits of a 16-bit mono WAV or AIFF file.

    This function extracts the message embedded in the sample data, assuming it is prefixed with a 32-bit integer representing its length. The message is decoded from the LSBs of each 16-bit sample.

    Args:
        input_path (str): Path to the audio file with embedded stego data.

    Returns:
        str: The decoded UTF-8 message.

    Raises:
        FileNotFoundError: If the file does not exist.
        UnsupportedFormatError: If the audio format is not 16-bit mono PCM.
        InvalidStegoDataError: If the message is invalid, corrupted, or cut off.
    """
    return _core.decode(input_path)
