from stegopy.audio import _core

def encode(input_path: str, output_path: str, message: str) -> None:
    """
    LSB encoding wrapper for 16-bit mono WAV files.
    """
    _core.encode(input_path, output_path, message)

def decode(input_path: str) -> str:
    """
    LSB decoding wrapper for 16-bit mono WAV files.
    """
    return _core.decode(input_path)
