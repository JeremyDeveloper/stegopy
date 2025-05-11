import os
from typing import List, Optional
from PIL import Image, ImageSequence, UnidentifiedImageError
from stegopy.utils import (
    _int_to_bits, _bits_to_int, _text_to_bits, _bits_to_text, _image_to_bits, _bits_to_image, _is_image_file
)
from stegopy.errors import (
    UnsupportedFormatError, PayloadTooLargeError, InvalidStegoDataError
)

def _validate_channel(channel: Optional[str]) -> Optional[int]:
    """
    Validates and converts a string channel name to an integer index.

    Args:
        channel (Optional[str]): Channel name ("r", "g", or "b") or None.

    Returns:
        Optional[int]: Index corresponding to channel or None.

    Raises:
        ValueError: If the channel is not valid.
    """
    if channel is None:
        return None
    channel = channel.lower()
    if channel not in ("r", "g", "b"):
        raise ValueError("Channel must be one of: 'r', 'g', 'b'")
    return {"r": 0, "g": 1, "b": 2}[channel]

def _get_region_indices(width: int, height: int, region: Optional[str]) -> List[tuple]:
    """
    Computes pixel coordinate tuples within a region of the image.

    Args:
        width (int): Image width.
        height (int): Image height.
        region (Optional[str]): Region name or None for full image.

    Returns:
        List[tuple]: List of (x, y) tuples representing pixel coordinates.

    Raises:
        ValueError: If region name is not supported.
    """
    if not region:
        return [(x, y) for y in range(height) for x in range(width)]

    region = region.lower()
    x_half = width // 2
    y_half = height // 2

    if region == "center":
        x_start, x_end = width // 4, width // 4 + x_half
        y_start, y_end = height // 4, height // 4 + y_half
    elif region == "topleft":
        x_start, x_end = 0, x_half
        y_start, y_end = 0, y_half
    elif region == "topright":
        x_start, x_end = x_half, width
        y_start, y_end = 0, y_half
    elif region == "bottomleft":
        x_start, x_end = 0, x_half
        y_start, y_end = y_half, height
    elif region == "bottomright":
        x_start, x_end = x_half, width
        y_start, y_end = y_half, height
    else:
        raise ValueError("Unsupported region type. Use: center, topleft, topright, bottomleft, bottomright.")

    return [(x, y) for y in range(y_start, y_end) for x in range(x_start, x_end)]

def encode(
    image_path: str,
    output_path: str,
    payload: str,
    frame: Optional[int] = None,
    region: Optional[str] = None,
    channel: Optional[str] = None,
    alpha: Optional[bool] = False,
) -> None:
    """
    Encodes a payload into the LSB of the image.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path where the stego image will be saved.
        payload (str): Payload to embed.
        frame (Optional[int]): Target frame index for animated images (e.g. GIF).
        region (Optional[str]): Region of the image to embed into.
        channel (Optional[str]): Specific RGB channel to use.
        alpha (Optional[bool]): Whether to use the alpha channel.
        
    Raises:
        FileNotFoundError: If input image does not exist.
        UnsupportedFormatError: If image cannot be read or is invalid.
        PayloadTooLargeError: If payload exceeds capacity.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    if not _is_image_file(image_path):
        raise UnsupportedFormatError(f"Unsupported image format: {image_path}")

    try:
        img = Image.open(image_path)
    except UnidentifiedImageError:
        raise UnsupportedFormatError("Unsupported or invalid image file.")

    if frame is not None:
        frames = [f.copy() for f in ImageSequence.Iterator(img)]
        if not (0 <= frame < len(frames)):
            raise ValueError(f"Frame {frame} is out of range. File has {len(frames)} frames.")
        try:
            img.seek(frame)
        except EOFError:
            raise UnsupportedFormatError("Unsupported or invalid image file.")
        img = img.copy()

    img = img.convert("RGBA" if alpha else "RGB")
    width, height = img.size
    pixels = img.load()
    indices = _get_region_indices(width, height, region)
    channel_idx = _validate_channel(channel)
    msg_type = "T"
    
    if os.path.exists(payload) and _is_image_file(payload):
        msg_type = "I"
        msg_bits = _image_to_bits(Image.open(payload))
        length_bits = _int_to_bits(len(msg_bits) // 8, 32)    
    else: 
        msg_bits = _text_to_bits(payload)
        length_bits = _int_to_bits(len(payload.encode('utf-8')), 32)
    
    msg_bits = length_bits + _int_to_bits(ord(msg_type), 8) + msg_bits
    capacity = (len(indices) * (1 if channel or alpha else 3)) // 8 - 5

    if len(msg_bits) > capacity:
        raise PayloadTooLargeError(f"Payload too large. Only {capacity} bits available.")

    bit_index = 0
    for x, y in indices:
        pixel = list(pixels[x, y])
        if channel_idx is not None:
            if bit_index < len(msg_bits):
                pixel[channel_idx] = (pixel[channel_idx] & ~1) | msg_bits[bit_index]
                bit_index += 1
        elif alpha:
            if bit_index < len(msg_bits):
                pixel[3] = (pixel[3] & ~1) | msg_bits[bit_index]
                bit_index += 1
        else:
            for i in range(3):
                if bit_index < len(msg_bits):
                    pixel[i] = (pixel[i] & ~1) | msg_bits[bit_index]
                    bit_index += 1
        pixels[x, y] = tuple(pixel)

    save_kwargs = {}
    ext = os.path.splitext(output_path)[1].lower()
    if ext == ".webp":
        save_kwargs["lossless"] = True
    elif ext == ".tiff":
        save_kwargs["compression"] = "none"

    if frame is not None:
        frames[frame] = img
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:]
        )
    else: img.save(output_path, **save_kwargs)

def decode(
    image_path: str,
    frame: Optional[int] = None,
    region: Optional[str] = None,
    channel: Optional[str] = None,
    alpha: Optional[bool] = False
) -> str:
    """
    Decodes a payload from the LSBs of the image.

    Args:
        image_path (str): Image file containing stego data.
        frame (Optional[int]): Target frame index for animated images (e.g. GIF).
        region (Optional[str]): Region used during encoding.
        channel (Optional[str]): Channel used during encoding.
        alpha (Optional[bool]): If payload was encoded in alpha channel.

    Returns:
        str: The decoded payload.

    Raises:
        FileNotFoundError: If file does not exist.
        UnsupportedFormatError: If image format is invalid.
        InvalidStegoDataError: If payload is corrupted or incomplete.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    if not _is_image_file(image_path):
        raise UnsupportedFormatError(f"Unsupported image format: {image_path}")

    try:
        img = Image.open(image_path)
    except UnidentifiedImageError:
        raise UnsupportedFormatError("Unsupported or invalid image file.")
    
    if frame is not None:
        try:
            img.seek(frame)
        except EOFError:
            raise UnsupportedFormatError("Unsupported or invalid image file.")

    img = img.convert("RGBA" if alpha else "RGB")
    width, height = img.size
    pixels = img.load()
    indices = _get_region_indices(width, height, region)
    channel_idx = _validate_channel(channel)

    bits = []
    for x, y in indices:
        pixel = pixels[x, y]
        if channel_idx is not None:
            bits.append(pixel[channel_idx] & 1)
        elif alpha:
            bits.append(pixel[3] & 1)
        else:
            bits.extend((pixel[0] & 1, pixel[1] & 1, pixel[2] & 1))

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
