import unittest
import numpy as np
from datamatrix_payload.core import bytes_to_symbols, symbols_to_bytes, rgb_to_int, int_to_rgb, palette, render, sample, detect
from datamatrix_payload import rs32


class VisualPayloadTests(unittest.TestCase):
    def test_arbitrary_binary_payload_and_padding(self):
        for length in [1, 2, 5, 31, 256, 1023]:
            original = bytes(i % 256 for i in range(length))
            for bits in [1, 5, 7, 8]:
                self.assertEqual(symbols_to_bytes(bytes_to_symbols(original, bits), bits, length), original)

    def test_hexadecimal_equivalence_and_invalid_inputs(self):
        self.assertEqual(rgb_to_int((255, 128, 0)), 0xFF8000)
        for value in [0, 0xFF8000, 0xFFFFFF, 0x123456]:
            self.assertEqual(rgb_to_int(int_to_rgb(value)), value)
        for value in [-1, 2**24]:
            with self.assertRaises(ValueError): int_to_rgb(value)

    def test_all_palette_symbols_survive_exact_rendering(self):
        for q in [8, 16, 32, 64, 128, 256]:
            data = np.arange(256) % q
            for s in [1, 2, 4]:
                rgb = render(data, palette(q), 16, s)
                np.testing.assert_array_equal(detect(sample(rgb, 16, s), palette(q)), data)

    def test_erased_symbol_values_cannot_affect_reconstruction(self):
        rng = np.random.default_rng(9131)
        for count in range(9):
            for _ in range(5):
                message = rng.integers(0, 32, 23, dtype=np.uint8)
                codeword = rs32.encode(message)
                locations = rng.choice(31, count, replace=False)
                codeword[locations] = rng.integers(0, 32, count, dtype=np.uint8)
                np.testing.assert_array_equal(rs32.decode_erasures(codeword, locations), message)

    def test_more_than_eight_erasures_are_refused(self):
        with self.assertRaises(ValueError):
            rs32.decode_erasures(rs32.encode(np.arange(23)), list(range(9)))

    def test_unknown_error_is_not_silently_accepted_when_redundancy_detects_it(self):
        encoded = rs32.encode(np.arange(23))
        encoded[0] ^= 1
        with self.assertRaises(ValueError): rs32.decode_erasures(encoded, [])

    def test_rs_stream_preserves_non_aligned_length(self):
        original = bytes_to_symbols(b"DataMatrix payload: binary \x00\xFF" * 5)
        coded, count = rs32.encode_stream(original)
        np.testing.assert_array_equal(rs32.decode_stream(coded, count), original)

    def test_out_of_alphabet_stream_values_are_rejected_before_casting(self):
        for invalid in [np.array([256]), np.array([-1]), np.array([1.5])]:
            with self.assertRaises(ValueError): rs32.encode_stream(invalid)


if __name__ == "__main__": unittest.main()
