# unicode-animations

Python port of [gunnargray-dev/unicode-animations](https://github.com/gunnargray-dev/unicode-animations).

18 pre-built Unicode braille spinner animations as raw frame data, plus grid utilities for building custom spinners. Zero dependencies.

## Install

```
pip install unicode-animations
```

## Usage

```python
from unicode_animations import spinners

spinner = spinners["helix"]
print(spinner.frames)    # tuple of animation frames
print(spinner.interval)  # ms between frames
```

### Custom spinners with the grid API

```python
from unicode_animations import make_grid, grid_to_braille

grid = make_grid(4, 2)   # 4 rows × 2 cols (one braille char)
grid[0][0] = True
grid[3][1] = True
print(grid_to_braille(grid))  # ⡁
```

### CLI demo

```
python -m unicode_animations          # cycle through all spinners
python -m unicode_animations helix    # preview one
python -m unicode_animations --list   # list all names
```

## Available spinners

`braille` · `braillewave` · `dna` · `scan` · `rain` · `scanline` · `pulse` · `snake` · `sparkle` · `cascade` · `columns` · `orbit` · `breathe` · `waverows` · `checkerboard` · `helix` · `fillsweep` · `diagswipe`

## License

MIT
