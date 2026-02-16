"""
Unicode Braille Spinners

A collection of animated unicode spinners built on braille characters (U+2800 block).
Each braille char is a 2x4 dot grid — these generators compose them into
multi-character animated frames for use as loading indicators.
"""

from __future__ import annotations

import math
from typing import Literal, NamedTuple

# ── Types ──────────────────────────────────────────────────────────────


class Spinner(NamedTuple):
    frames: tuple[str, ...]
    interval: int


BrailleSpinnerName = Literal[
    "braille", "braillewave", "dna",
    "scan", "rain", "scanline", "pulse", "snake",
    "sparkle", "cascade", "columns", "orbit", "breathe",
    "waverows", "checkerboard", "helix", "fillsweep", "diagswipe",
]

# ── Braille Grid Utility ──────────────────────────────────────────────
#
#   Each braille char is a 2-col × 4-row dot grid.
#   Dot numbering & bit values:
#     Row 0:  dot1 (0x01)  dot4 (0x08)
#     Row 1:  dot2 (0x02)  dot5 (0x10)
#     Row 2:  dot3 (0x04)  dot6 (0x20)
#     Row 3:  dot7 (0x40)  dot8 (0x80)
#
#   Base codepoint: U+2800

BRAILLE_DOT_MAP = [
    [0x01, 0x08],  # row 0
    [0x02, 0x10],  # row 1
    [0x04, 0x20],  # row 2
    [0x40, 0x80],  # row 3
]


def grid_to_braille(grid: list[list[bool]]) -> str:
    """Convert a 2D boolean grid into a braille string.

    grid[row][col] = True means dot is raised.
    Width must be even (2 dot-columns per braille char).
    """
    rows = len(grid)
    cols = len(grid[0]) if grid else 0
    char_count = math.ceil(cols / 2)
    result: list[str] = []
    for c in range(char_count):
        code = 0x2800
        for r in range(min(4, rows)):
            for d in range(2):
                col = c * 2 + d
                if col < cols and r < len(grid) and grid[r][col]:
                    code |= BRAILLE_DOT_MAP[r][d]
        result.append(chr(code))
    return "".join(result)


def make_grid(rows: int, cols: int) -> list[list[bool]]:
    """Create an empty grid of given dimensions."""
    if rows <= 0 or cols <= 0:
        return []
    return [[False] * cols for _ in range(rows)]


# ── Frame Generators ──────────────────────────────────────────────────


def _gen_scan() -> tuple[str, ...]:
    W, H = 8, 4
    frames: list[str] = []
    for pos in range(-1, W + 1):
        g = make_grid(H, W)
        for r in range(H):
            for c in range(W):
                if c == pos or c == pos - 1:
                    g[r][c] = True
        frames.append(grid_to_braille(g))
    return tuple(frames)


def _gen_rain() -> tuple[str, ...]:
    W, H, total_frames = 8, 4, 12
    offsets = [0, 3, 1, 5, 2, 7, 4, 6]
    frames: list[str] = []
    for f in range(total_frames):
        g = make_grid(H, W)
        for c in range(W):
            row = (f + offsets[c]) % (H + 2)
            if row < H:
                g[row][c] = True
        frames.append(grid_to_braille(g))
    return tuple(frames)


def _gen_scan_line() -> tuple[str, ...]:
    W, H = 6, 4
    positions = [0, 1, 2, 3, 2, 1]
    frames: list[str] = []
    for row in positions:
        g = make_grid(H, W)
        for c in range(W):
            g[row][c] = True
            if row > 0:
                g[row - 1][c] = c % 2 == 0
        frames.append(grid_to_braille(g))
    return tuple(frames)


def _gen_pulse() -> tuple[str, ...]:
    W, H = 6, 4
    cx = W / 2 - 0.5
    cy = H / 2 - 0.5
    radii = [0.5, 1.2, 2, 3, 3.5]
    frames: list[str] = []
    for radius in radii:
        g = make_grid(H, W)
        for row in range(H):
            for col in range(W):
                dist = math.sqrt((col - cx) ** 2 + (row - cy) ** 2)
                if abs(dist - radius) < 0.9:
                    g[row][col] = True
        frames.append(grid_to_braille(g))
    return tuple(frames)


def _gen_snake() -> tuple[str, ...]:
    W, H = 4, 4
    path: list[tuple[int, int]] = []
    for r in range(H):
        if r % 2 == 0:
            for c in range(W):
                path.append((r, c))
        else:
            for c in range(W - 1, -1, -1):
                path.append((r, c))
    frames: list[str] = []
    for i in range(len(path)):
        g = make_grid(H, W)
        for t in range(4):
            idx = (i - t + len(path)) % len(path)
            g[path[idx][0]][path[idx][1]] = True
        frames.append(grid_to_braille(g))
    return tuple(frames)


def _gen_sparkle() -> tuple[str, ...]:
    patterns = [
        [1,0,0,1,0,0,1,0, 0,0,1,0,0,1,0,0, 0,1,0,0,1,0,0,1, 1,0,0,0,0,1,0,0],
        [0,1,0,0,1,0,0,1, 1,0,0,1,0,0,0,1, 0,0,0,1,0,1,0,0, 0,0,1,0,1,0,1,0],
        [0,0,1,0,0,1,0,0, 0,1,0,0,0,0,1,0, 1,0,1,0,0,0,0,1, 0,1,0,1,0,0,0,1],
        [1,0,0,0,0,0,1,1, 0,0,1,0,1,0,0,0, 0,0,0,0,1,0,1,0, 1,0,0,1,0,0,1,0],
        [0,0,0,1,1,0,0,0, 0,1,0,0,0,1,0,1, 1,0,0,1,0,0,0,0, 0,1,0,0,0,1,0,1],
        [0,1,1,0,0,0,0,1, 0,0,0,1,0,0,1,0, 0,1,0,0,0,1,0,0, 0,0,1,0,1,0,0,0],
    ]
    W, H = 8, 4
    frames: list[str] = []
    for pat in patterns:
        g = make_grid(H, W)
        for r in range(H):
            for c in range(W):
                g[r][c] = bool(pat[r * W + c])
        frames.append(grid_to_braille(g))
    return tuple(frames)


def _gen_cascade() -> tuple[str, ...]:
    W, H = 8, 4
    frames: list[str] = []
    for offset in range(-2, W + H):
        g = make_grid(H, W)
        for r in range(H):
            for c in range(W):
                diag = c + r
                if diag == offset or diag == offset - 1:
                    g[r][c] = True
        frames.append(grid_to_braille(g))
    return tuple(frames)


def _gen_columns() -> tuple[str, ...]:
    W, H = 6, 4
    frames: list[str] = []
    for col in range(W):
        for fill_to in range(H - 1, -1, -1):
            g = make_grid(H, W)
            for pc in range(col):
                for r in range(H):
                    g[r][pc] = True
            for r in range(fill_to, H):
                g[r][col] = True
            frames.append(grid_to_braille(g))
    full = make_grid(H, W)
    for r in range(H):
        for c in range(W):
            full[r][c] = True
    frames.append(grid_to_braille(full))
    frames.append(grid_to_braille(make_grid(H, W)))
    return tuple(frames)


def _gen_orbit() -> tuple[str, ...]:
    W, H = 2, 4
    path: list[tuple[int, int]] = [
        (0, 0), (0, 1),
        (1, 1), (2, 1), (3, 1),
        (3, 0),
        (2, 0), (1, 0),
    ]
    frames: list[str] = []
    for i in range(len(path)):
        g = make_grid(H, W)
        g[path[i][0]][path[i][1]] = True
        t1 = (i - 1 + len(path)) % len(path)
        g[path[t1][0]][path[t1][1]] = True
        frames.append(grid_to_braille(g))
    return tuple(frames)


def _gen_breathe() -> tuple[str, ...]:
    stages: list[list[tuple[int, int]]] = [
        [],
        [(1, 0)],
        [(0, 1), (2, 0)],
        [(0, 0), (1, 1), (3, 0)],
        [(0, 0), (1, 1), (2, 0), (3, 1)],
        [(0, 0), (0, 1), (1, 1), (2, 0), (3, 1)],
        [(0, 0), (0, 1), (1, 0), (2, 1), (3, 0), (3, 1)],
        [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (3, 0), (3, 1)],
        [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)],
    ]
    sequence = stages + list(reversed(stages))[1:]
    frames: list[str] = []
    for dots in sequence:
        g = make_grid(4, 2)
        for r, c in dots:
            g[r][c] = True
        frames.append(grid_to_braille(g))
    return tuple(frames)


def _gen_wave_rows() -> tuple[str, ...]:
    W, H, total_frames = 8, 4, 16
    frames: list[str] = []
    for f in range(total_frames):
        g = make_grid(H, W)
        for c in range(W):
            phase = f - c * 0.5
            row = round((math.sin(phase * 0.8) + 1) / 2 * (H - 1))
            g[row][c] = True
            if row > 0:
                g[row - 1][c] = (f + c) % 3 == 0
        frames.append(grid_to_braille(g))
    return tuple(frames)


def _gen_checkerboard() -> tuple[str, ...]:
    W, H = 6, 4
    frames: list[str] = []
    for phase in range(4):
        g = make_grid(H, W)
        for r in range(H):
            for c in range(W):
                if phase < 2:
                    g[r][c] = (r + c + phase) % 2 == 0
                else:
                    g[r][c] = (r + c + phase) % 3 == 0
        frames.append(grid_to_braille(g))
    return tuple(frames)


def _gen_helix() -> tuple[str, ...]:
    W, H, total_frames = 8, 4, 16
    frames: list[str] = []
    for f in range(total_frames):
        g = make_grid(H, W)
        for c in range(W):
            phase = (f + c) * (math.pi / 4)
            y1 = round((math.sin(phase) + 1) / 2 * (H - 1))
            y2 = round((math.sin(phase + math.pi) + 1) / 2 * (H - 1))
            g[y1][c] = True
            g[y2][c] = True
        frames.append(grid_to_braille(g))
    return tuple(frames)


def _gen_fill_sweep() -> tuple[str, ...]:
    W, H = 4, 4
    frames: list[str] = []
    for row in range(H - 1, -1, -1):
        g = make_grid(H, W)
        for r in range(row, H):
            for c in range(W):
                g[r][c] = True
        frames.append(grid_to_braille(g))
    full = make_grid(H, W)
    for r in range(H):
        for c in range(W):
            full[r][c] = True
    frames.append(grid_to_braille(full))
    frames.append(grid_to_braille(full))
    for row in range(H):
        g = make_grid(H, W)
        for r in range(row + 1, H):
            for c in range(W):
                g[r][c] = True
        frames.append(grid_to_braille(g))
    frames.append(grid_to_braille(make_grid(H, W)))
    return tuple(frames)


def _gen_diagonal_swipe() -> tuple[str, ...]:
    W, H = 4, 4
    max_diag = W + H - 2
    frames: list[str] = []
    for d in range(max_diag + 1):
        g = make_grid(H, W)
        for r in range(H):
            for c in range(W):
                if r + c <= d:
                    g[r][c] = True
        frames.append(grid_to_braille(g))
    full = make_grid(H, W)
    for r in range(H):
        for c in range(W):
            full[r][c] = True
    frames.append(grid_to_braille(full))
    for d in range(max_diag + 1):
        g = make_grid(H, W)
        for r in range(H):
            for c in range(W):
                if r + c > d:
                    g[r][c] = True
        frames.append(grid_to_braille(g))
    frames.append(grid_to_braille(make_grid(H, W)))
    return tuple(frames)


# ── Spinner Registry ──────────────────────────────────────────────────

spinners: dict[BrailleSpinnerName, Spinner] = {
    # Classic braille single-char
    "braille": Spinner(
        frames=("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"),
        interval=80,
    ),
    "braillewave": Spinner(
        frames=(
            "⠁⠂⠄⡀",
            "⠂⠄⡀⢀",
            "⠄⡀⢀⠠",
            "⡀⢀⠠⠐",
            "⢀⠠⠐⠈",
            "⠠⠐⠈⠁",
            "⠐⠈⠁⠂",
            "⠈⠁⠂⠄",
        ),
        interval=100,
    ),
    "dna": Spinner(
        frames=(
            "⠋⠉⠙⠚",
            "⠉⠙⠚⠒",
            "⠙⠚⠒⠂",
            "⠚⠒⠂⠂",
            "⠒⠂⠂⠒",
            "⠂⠂⠒⠲",
            "⠂⠒⠲⠴",
            "⠒⠲⠴⠤",
            "⠲⠴⠤⠄",
            "⠴⠤⠄⠋",
            "⠤⠄⠋⠉",
            "⠄⠋⠉⠙",
        ),
        interval=80,
    ),
    # Generated braille grid animations
    "scan": Spinner(frames=_gen_scan(), interval=70),
    "rain": Spinner(frames=_gen_rain(), interval=100),
    "scanline": Spinner(frames=_gen_scan_line(), interval=120),
    "pulse": Spinner(frames=_gen_pulse(), interval=180),
    "snake": Spinner(frames=_gen_snake(), interval=80),
    "sparkle": Spinner(frames=_gen_sparkle(), interval=150),
    "cascade": Spinner(frames=_gen_cascade(), interval=60),
    "columns": Spinner(frames=_gen_columns(), interval=60),
    "orbit": Spinner(frames=_gen_orbit(), interval=100),
    "breathe": Spinner(frames=_gen_breathe(), interval=100),
    "waverows": Spinner(frames=_gen_wave_rows(), interval=90),
    "checkerboard": Spinner(frames=_gen_checkerboard(), interval=250),
    "helix": Spinner(frames=_gen_helix(), interval=80),
    "fillsweep": Spinner(frames=_gen_fill_sweep(), interval=100),
    "diagswipe": Spinner(frames=_gen_diagonal_swipe(), interval=60),
}
