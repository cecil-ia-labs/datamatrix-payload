"""Behavioural checks for the hexadecimal GIF research profile."""
import io
import unittest
import numpy as np
from PIL import Image
from qddm import (
    DEFAULT_PALETTE, Profile, encode, decode, inspect, pack_address,
    unpack_address, scalar_to_hex, hex_to_scalar, scalar_to_dimensions,
    dimensions_to_scalar,
)

class HexGifTests(unittest.TestCase):
    def test_variable_lengths_and_zero_octets_round_trip(self):
        for original in ("", "00", "0000", "00FF0080", bytes(range(256)).hex()):
            result = encode(original)
            self.assertEqual(decode(result.gif, payload_bytes=len(original)//2), original.upper())

    def test_palette_values_and_order_survive_each_frame(self):
        palettes = [DEFAULT_PALETTE[i:] + DEFAULT_PALETTE[:i] for i in range(4)]
        source = bytes(range(256)).hex() * 12
        result = encode(source, frames=4, palettes=palettes)
        self.assertEqual([f.palette_hex for f in inspect(result.gif)], palettes)
        self.assertEqual(decode(result.gif, payload_bytes=len(source)//2), source.upper())

    def test_identical_frames_remain_separate_states(self):
        result = encode("00", frames=16)
        self.assertEqual(len(inspect(result.gif)), 16)
        self.assertEqual(sum(f.delay_cs for f in inspect(result.gif)), 200)

    def test_maximum_profile_and_capacity(self):
        rng = np.random.default_rng(20261104)
        source = rng.integers(0, 256, 196608, dtype=np.uint8).tobytes().hex()
        result = encode(source, frames=64)
        self.assertEqual((result.frame_count,result.colors,result.duration_ms),(64,64,8000))
        self.assertEqual(decode(result.gif,payload_bytes=196608),source.upper())
        with Image.open(io.BytesIO(result.gif)) as image:
            self.assertEqual(image.size,(256,256))
            self.assertEqual(image.n_frames,64)
        with self.assertRaises(ValueError):
            encode(source+"00")

    def test_slow_state_cadence(self):
        result=encode("0041",frames=2,frame_period_ms=60000)
        self.assertEqual([f.delay_cs for f in inspect(result.gif)],[6000,6000])

    def test_profile_palette_and_hexadecimal_bounds(self):
        for count in (0,65):
            with self.assertRaises(ValueError): encode("00",frames=count)
        for colors in ([DEFAULT_PALETTE[0]]*64,["#GG0000","#FFFFFF"],
                       [f"#{i:06X}" for i in range(128)]):
            with self.assertRaises(ValueError): encode("00",palettes=[colors])
        for source in ("0","0x00","GG","00 01"):
            with self.assertRaises(ValueError): encode(source)
        with self.assertRaises(ValueError): Profile(pixel_side=128)

    def test_truncated_or_invalid_gif_is_rejected(self):
        original=encode("000102").gif
        for raw in (b"",b"not a GIF",original[:20],original[:-1],original+b"\0"):
            with self.assertRaises(ValueError): decode(raw)

    def test_inconsistent_effective_module_is_rejected(self):
        indices=bytearray(256*256)
        indices[1]=1
        image=Image.frombytes("P",(256,256),bytes(indices))
        image.putpalette(bytes.fromhex("".join(v[1:] for v in DEFAULT_PALETTE)))
        stream=io.BytesIO()
        image.save(stream,format="GIF",optimize=False,interlace=False)
        with self.assertRaisesRegex(ValueError,"inconsistent"): decode(stream.getvalue())

    def test_catalogue_addresses_preserve_four_coordinates(self):
        self.assertEqual(pack_address(63,63,63,63),"0xFFFFFF")
        rng=np.random.default_rng(64)
        for row in rng.integers(0,64,(300,4)):
            coordinates=tuple(int(x) for x in row)
            self.assertEqual(unpack_address(pack_address(*coordinates)),coordinates)
        with self.assertRaises(ValueError): pack_address(64,0,0,0)

    def test_unicode_scalar_boundaries_and_injective_mapping(self):
        boundary=[0,0x41,0xE3,0x20AC,0xD7FF,0xE000,0xFFFF,0x10000,0x1F600,0x10FFFF]
        rng=np.random.default_rng(1112064)
        values=boundary+[int(x) for x in rng.integers(0,0x110000,1000)
                         if not 0xD800<=x<=0xDFFF]
        for value in values:
            self.assertEqual(hex_to_scalar(scalar_to_hex(value)),value)
            self.assertEqual(dimensions_to_scalar(scalar_to_dimensions(value)),value)
        self.assertEqual(scalar_to_dimensions(0x41),("0x00","0x00","0x01","0x01"))
        for value in (-1,0xD800,0xDFFF,0x110000):
            with self.assertRaises(ValueError): scalar_to_hex(value)
        with self.assertRaises(ValueError):
            dimensions_to_scalar(("0x00","0x00","0x40","0x00"))

if __name__=="__main__":
    unittest.main()

