from stegopy.image import _core
from typing import Optional

def encode(image_path: str, output_path: str, message: str, region: Optional[str] = None, channel: Optional[str] = None, alpha: Optional[bool] = False) -> None:
    _core.encode(image_path, output_path, message, region=region, channel=channel, alpha=alpha)

def decode(image_path: str, region: Optional[str] = None, channel: Optional[str] = None, alpha: Optional[bool] = False) -> str:
    return _core.decode(image_path, region=region, channel=channel, alpha=alpha)
