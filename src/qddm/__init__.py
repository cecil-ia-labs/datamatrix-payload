# SPDX-FileCopyrightText: 2026 Cecil-IA Labs
# SPDX-License-Identifier: MIT
#
# Author: João Paulo De Luca Jr.; Jorge Luiz Espanhol
# Organization: Cecil-IA Labs
# Project: Quad-Dimensional DataMatrix
#
# AI-assisted development:
# OpenAI ChatGPT and Codex were used as development tools.
# Human-directed development and integration.
# No OpenAI sponsorship, affiliation, or endorsement is implied.
#
# License: See the repository LICENSE file and SPDX identifier above.

"""Quad-Dimensional DataMatrix: exploratory hexadecimal GIF transport."""
from .hexgif import (
    AUTHORS, TITLE, DEFAULT_PALETTE, Encoding, Frame, Profile,
    encode, decode, inspect, single_frame_gif, unpack_dimensions,
    pack_dimensions, pack_address, unpack_address,
    scalar_to_hex, hex_to_scalar, scalar_to_dimensions, dimensions_to_scalar,
)

__version__ = "0.2.0"

