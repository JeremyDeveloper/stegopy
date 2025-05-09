import os, struct
from stegopy.utils import (
    _int_to_bits, _bits_to_int, _text_to_bits, _bits_to_text, _image_to_bits, _bits_to_image, _open_audio, _is_image_file
)
from stegopy.errors import (
    UnsupportedFormatError, PayloadTooLargeError, InvalidStegoDataError
)
from PIL import Image

def encode(input_path: str, output_path: str, payload: str) -> None:
    """
    Encode a payload into the LSB of each 16-bit sample in a mono WAV or AIFF file.

    This function uses lossless audio bit manipulation to hide the payload directly in the sample data.

    Args:
        input_path (str): Path to the input WAV or AIFF file.
        output_path (str): Output path for the stego audio file.
        payload (str): Payload to embed.

    Raises:
        FileNotFoundError: If the audio file does not exist.
        UnsupportedFormatError: If the file is not 16-bit mono PCM.
        PayloadTooLargeError: If the payload exceeds available LSB capacity.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Audio file not found: {input_path}")

    with _open_audio(input_path, 'rb') as audio:
        params = audio.getparams()
        if params.sampwidth != 2 or params.nchannels != 1:
            raise UnsupportedFormatError("Only 16-bit mono PCM WAV files are supported.")
        frames = bytearray(audio.readframes(audio.getnframes()))
    msg_type = "T"
    
    if os.path.exists(payload) and _is_image_file(payload):
        msg_type = "I"
        msg_bits = _image_to_bits(Image.open(payload))
        length_bits = _int_to_bits(len(msg_bits) // 8, 32)    
    else: 
        msg_bits = _text_to_bits(payload)
        length_bits = _int_to_bits(len(payload.encode('utf-8')), 32)
    
    msg_bits = length_bits + _int_to_bits(ord(msg_type), 8) + msg_bits

    if len(msg_bits) > len(frames) // 2:
        raise PayloadTooLargeError("Payload is too large to fit in this audio.")

    for i, bit in enumerate(msg_bits):
        byte_index = i * 2
        sample = struct.unpack('<h', frames[byte_index:byte_index+2])[0]
        sample = (sample & ~1) | bit
        frames[byte_index:byte_index+2] = struct.pack('<h', sample)

    with _open_audio(output_path, 'wb') as out:
        out.setparams(params)
        out.writeframes(frames)

def decode(input_path: str) -> str:
    """
    Decode a payload from the least significant bits of a 16-bit mono WAV or AIFF file.

    The payload is assumed to be prefixed with a 32-bit integer representing its length.

    Args:
        input_path (str): Path to the audio file with embedded stego data.

    Returns:
        str: The decoded payload.

    Raises:
        FileNotFoundError: If the file does not exist.
        UnsupportedFormatError: If the audio format is not 16-bit mono PCM.
        InvalidStegoDataError: If the payload is invalid, corrupted, or cut off.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Audio file not found: {input_path}")

    with _open_audio(input_path, 'rb') as audio:
        params = audio.getparams()
        if params.sampwidth != 2 or params.nchannels != 1:
            raise UnsupportedFormatError("Only 16-bit mono PCM WAV files are supported.")
        frames = bytearray(audio.readframes(audio.getnframes()))

    bits = [(struct.unpack('<h', frames[i:i+2])[0] & 1) for i in range(0, len(frames), 2)]

    msg_len = _bits_to_int(bits[:32])
    msg_type = chr(_bits_to_int(bits[32:40]))
    msg_bits = bits[40:40 + (msg_len * 8)]

    if len(msg_bits) < msg_len * 8:
        raise InvalidStegoDataError("Payload appears to be incomplete or corrupted.")

    if msg_type == "T":
        return _bits_to_text(msg_bits)
    elif msg_type == "I":
        return _bits_to_image(msg_bits)

    raise InvalidStegoDataError("Payload appears to be incomplete or corrupted.")
