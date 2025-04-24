from stegopy.image import _core

def encode(image_path: str, output_path: str, message: str) -> None:
    _core.encode(image_path, output_path, message, alpha=True)

def decode(image_path: str) -> str:
    return _core.decode(image_path, alpha=True)
