class StegopyError(Exception):
    """Base class for all stegopy-related errors."""
    pass

class UnsupportedFormatError(StegopyError):
    """Raised when a file format is not supported for steganography."""
    pass

class PayloadTooLargeError(StegopyError):
    """Raised when the message or data cannot fit into the medium (image, audio, etc.)."""
    pass

class InvalidStegoDataError(StegopyError):
    """Raised when decoded data is invalid or corrupted."""
    pass