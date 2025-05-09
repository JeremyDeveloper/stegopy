from stegopy.audio import _core

def encode(input_path: str, output_path: str, payload: str) -> None:
    """
    Encodes a payload into the least significant bits of each 16-bit sample in a mono WAV or AIFF file.

    This function utilizes lossless audio bit manipulation to directly embed the payload within the sample data. The payload is prefixed with a 32-bit integer representing its length, ensuring accurate decoding.

    Args:
        input_path (str): Path to the input WAV or AIFF file.
        output_path (str): Output path for the stego audio file.
        payload (str): Payload to embed.

    Raises:
        FileNotFoundError: If the audio file does not exist.
        UnsupportedFormatError: If the file is not 16-bit mono PCM.
        PayloadTooLargeError: If the payload exceeds available LSB capacity.
    """
    _core.encode(input_path, output_path, payload)

def decode(input_path: str) -> str:
    """
    Decodes a payload from the least significant bits of a 16-bit mono WAV or AIFF file.

    This function extracts the payload embedded in the sample data, assuming it is prefixed with a 32-bit integer representing its length. The payload is decoded from the LSBs of each 16-bit sample.

    Args:
        input_path (str): Path to the audio file with embedded stego data.

    Returns:
        str: The decoded payload.

    Raises:
        FileNotFoundError: If the file does not exist.
        UnsupportedFormatError: If the audio format is not 16-bit mono PCM.
        InvalidStegoDataError: If the payload is invalid, corrupted, or cut off.
    """
    return _core.decode(input_path)
