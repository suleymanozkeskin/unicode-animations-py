import pytest

from unicode_animations.braille import spinners, grid_to_braille, make_grid, BrailleSpinnerName

ALL_NAMES: list[str] = [
    "braille", "braillewave", "dna",
    "scan", "rain", "scanline", "pulse", "snake",
    "sparkle", "cascade", "columns", "orbit", "breathe",
    "waverows", "checkerboard", "helix", "fillsweep", "diagswipe",
]


# ── make_grid ──────────────────────────────────────────────────────────


class TestMakeGrid:
    def test_correct_dimensions(self):
        g = make_grid(4, 8)
        assert len(g) == 4
        assert len(g[0]) == 8
        assert all(cell is False for row in g for cell in row)

    def test_zero_dimensions(self):
        assert make_grid(0, 5) == []
        assert make_grid(5, 0) == []

    def test_negative_dimensions(self):
        assert make_grid(-1, 5) == []
        assert make_grid(5, -1) == []


# ── grid_to_braille ───────────────────────────────────────────────────


class TestGridToBraille:
    def test_empty_grid(self):
        assert grid_to_braille([]) == ""

    def test_blank_braille_char(self):
        g = make_grid(4, 2)
        assert grid_to_braille(g) == "\u2800"

    def test_full_braille_char(self):
        g = make_grid(4, 2)
        for r in range(4):
            for c in range(2):
                g[r][c] = True
        assert grid_to_braille(g) == "\u28FF"

    def test_individual_dots(self):
        # dot1 (row0, col0) = 0x01
        g1 = make_grid(4, 2)
        g1[0][0] = True
        assert grid_to_braille(g1) == "\u2801"

        # dot4 (row0, col1) = 0x08
        g2 = make_grid(4, 2)
        g2[0][1] = True
        assert grid_to_braille(g2) == "\u2808"

        # dot2 (row1, col0) = 0x02
        g3 = make_grid(4, 2)
        g3[1][0] = True
        assert grid_to_braille(g3) == "\u2802"

        # dot5 (row1, col1) = 0x10
        g4 = make_grid(4, 2)
        g4[1][1] = True
        assert grid_to_braille(g4) == "\u2810"

        # dot3 (row2, col0) = 0x04
        g5 = make_grid(4, 2)
        g5[2][0] = True
        assert grid_to_braille(g5) == "\u2804"

        # dot6 (row2, col1) = 0x20
        g6 = make_grid(4, 2)
        g6[2][1] = True
        assert grid_to_braille(g6) == "\u2820"

        # dot7 (row3, col0) = 0x40
        g7 = make_grid(4, 2)
        g7[3][0] = True
        assert grid_to_braille(g7) == "\u2840"

        # dot8 (row3, col1) = 0x80
        g8 = make_grid(4, 2)
        g8[3][1] = True
        assert grid_to_braille(g8) == "\u2880"

    def test_multiple_characters(self):
        g = make_grid(4, 4)
        g[0][0] = True
        g[0][2] = True
        result = grid_to_braille(g)
        assert len(result) == 2
        assert result == "\u2801\u2801"

    def test_odd_width(self):
        g = make_grid(4, 3)
        g[0][0] = True
        g[0][2] = True
        result = grid_to_braille(g)
        assert len(result) == 2


# ── Spinners ──────────────────────────────────────────────────────────


class TestSpinners:
    def test_exports_all_18(self):
        assert sorted(spinners.keys()) == sorted(ALL_NAMES)

    @pytest.mark.parametrize("name", ALL_NAMES)
    def test_non_empty_frames(self, name: str):
        assert len(spinners[name].frames) > 0

    @pytest.mark.parametrize("name", ALL_NAMES)
    def test_positive_interval(self, name: str):
        assert spinners[name].interval > 0

    @pytest.mark.parametrize("name", ALL_NAMES)
    def test_consistent_frame_widths(self, name: str):
        widths = [len(list(f)) for f in spinners[name].frames]
        assert len(set(widths)) == 1
