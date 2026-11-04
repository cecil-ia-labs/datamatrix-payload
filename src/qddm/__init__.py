"""Quad-Dimensional DataMatrix: exploratory hexadecimal GIF transport."""
from .hexgif import (
    AUTHORS, TITLE, DEFAULT_PALETTE, Encoding, Frame, Profile,
    encode, decode, inspect, single_frame_gif, unpack_dimensions,
    pack_dimensions, pack_address, unpack_address,
    scalar_to_hex, hex_to_scalar, scalar_to_dimensions, dimensions_to_scalar,
)

__version__ = "0.2.0"

