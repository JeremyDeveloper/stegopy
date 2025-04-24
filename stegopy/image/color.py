from stegopy.image import _core

def encode(image_path: str, output_path: str, message: str, channel: str = "b") -> None:
    _core.encode(image_path, output_path, message, channel=channel)

def decode(image_path: str, channel: str = "b") -> str:
    return _core.decode(image_path, channel=channel)
