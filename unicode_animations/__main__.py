"""CLI demo: python -m unicode_animations [name | --list]"""

from __future__ import annotations

import argparse
import sys
import time

from .braille import scale_spinner, spinners
from .spinner import _COLORS


def _clear_rendered(line_count: int) -> None:
    for i in range(line_count):
        sys.stdout.write("\r\033[2K")
        if i < line_count - 1:
            sys.stdout.write("\033[1A")


def _preview(
    name: str, duration: float = 3.0, color: str | None = None, scale: int = 1
) -> None:
    spinner = spinners[name]  # type: ignore[index]
    if scale > 1:
        spinner = scale_spinner(spinner, scale)
    frames = spinner.frames
    interval = spinner.interval / 1000
    end = time.monotonic() + duration
    idx = 0
    line_count = 0
    label = f"  {name}: "

    split_frames = [frame.splitlines() or [""] for frame in frames]
    frame_width = max((len(line) for lines in split_frames for line in lines), default=0)
    frame_height = max((len(lines) for lines in split_frames), default=1)

    color_on = ""
    color_off = ""
    if color and sys.stdout.isatty():
        color_on = _COLORS.get(color, "")
        if color_on:
            color_off = "\033[0m"

    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    try:
        while time.monotonic() < end:
            _clear_rendered(line_count)
            lines = list(split_frames[idx % len(split_frames)])
            if len(lines) < frame_height:
                lines += [""] * (frame_height - len(lines))

            centered_lines = [line.center(frame_width) for line in lines]
            if color_on:
                centered_lines = [f"{color_on}{line}{color_off}" for line in centered_lines]

            output_lines = [f"{label}{centered_lines[0]}"]
            output_lines.extend(f"{' ' * len(label)}{line}" for line in centered_lines[1:])
            sys.stdout.write("\n".join(output_lines))
            sys.stdout.flush()
            line_count = len(output_lines)
            time.sleep(interval)
            idx += 1
    finally:
        _clear_rendered(line_count)
        sys.stdout.write("\033[?25h\n")
        sys.stdout.flush()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="unicode_animations",
        description="Preview Unicode braille spinner animations",
    )
    parser.add_argument("name", nargs="?", help="spinner name to preview")
    parser.add_argument(
        "-l", "--list", action="store_true", help="list available spinners"
    )
    parser.add_argument(
        "-d", "--duration", type=float, default=3.0, help="preview duration in seconds"
    )
    parser.add_argument(
        "-c", "--color", choices=sorted(_COLORS), help="colorize the preview"
    )
    parser.add_argument(
        "-s", "--scale", type=int, default=1, choices=[1, 2, 3],
        help="scale factor for bigger rendering (1-3)",
    )
    args = parser.parse_args()

    if args.list:
        for name, spinner in spinners.items():
            if args.scale > 1:
                spinner = scale_spinner(spinner, args.scale)
            sample_lines = (spinner.frames[0].splitlines() or [""])
            print(f"  {name:<16} {sample_lines[0]}")
            for line in sample_lines[1:]:
                print(f"  {'':<16} {line}")
        return

    if args.name:
        if args.name not in spinners:
            print(f"Unknown spinner: {args.name}")
            print(f"Available: {', '.join(spinners)}")
            sys.exit(1)
        try:
            _preview(args.name, duration=args.duration, color=args.color, scale=args.scale)
        except KeyboardInterrupt:
            sys.stdout.write("\033[?25h\n")
        return

    # Cycle through all spinners
    try:
        for name in spinners:
            _preview(name, duration=args.duration, color=args.color, scale=args.scale)
    except KeyboardInterrupt:
        sys.stdout.write("\033[?25h\n")


if __name__ == "__main__":
    main()
