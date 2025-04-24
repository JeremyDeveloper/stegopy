from stegopy.image import _core

def encode(image_path: str, output_path: str, message: str, region: str = "center") -> None:
    _core.encode(image_path, output_path, message, region=region)

def decode(image_path: str, region: str = "center") -> str:
    return _core.decode(image_path, region=region)
