"""CLI demo: python -m unicode_animations [name | --list]"""

from __future__ import annotations

import sys
import time

from .braille import spinners


def _preview(name: str, duration: float = 3.0) -> None:
    spinner = spinners[name]  # type: ignore[index]
    frames = spinner.frames
    interval = spinner.interval / 1000
    end = time.monotonic() + duration
    idx = 0
    sys.stdout.write(f"\033[?25l  {name}: ")
    sys.stdout.flush()
    try:
        while time.monotonic() < end:
            sys.stdout.write(f"\r  {name}: {frames[idx % len(frames)]}")
            sys.stdout.flush()
            time.sleep(interval)
            idx += 1
    finally:
        sys.stdout.write("\033[?25h\n")
        sys.stdout.flush()


def main() -> None:
    args = sys.argv[1:]

    if "--list" in args or "-l" in args:
        for name in spinners:
            print(name)
        return

    if args:
        name = args[0]
        if name not in spinners:
            print(f"Unknown spinner: {name}")
            print(f"Available: {', '.join(spinners)}")
            sys.exit(1)
        try:
            _preview(name, duration=5.0)
        except KeyboardInterrupt:
            sys.stdout.write("\033[?25h\n")
        return

    # Cycle through all spinners
    try:
        for name in spinners:
            _preview(name)
    except KeyboardInterrupt:
        sys.stdout.write("\033[?25h\n")


if __name__ == "__main__":
    main()
