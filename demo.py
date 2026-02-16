"""Demo showcasing unicode-animations features."""

from __future__ import annotations

import argparse
import sys
import time

from unicode_animations import LiveSpinner, live_spinner, spinners


def _dur(seconds: float, fast: bool) -> float:
    if not fast:
        return seconds
    return max(0.2, seconds * 0.3)


def run_demo(fast: bool = False) -> None:
    print("\n  === unicode-animations demo ===\n")

    # 1. Basic spinner with text
    with live_spinner("helix", text="Downloading files...", color="cyan"):
        time.sleep(_dur(3.0, fast))
    print("  ✓ Download complete\n")

    # 2. Cycle through a few spinners with different colors
    demos = [
        ("dna", "green", "Sequencing DNA..."),
        ("orbit", "yellow", "Calculating orbit..."),
        ("rain", "blue", "Fetching weather data..."),
        ("pulse", "magenta", "Scanning network..."),
        ("snake", "red", "Defragmenting..."),
    ]

    for name, color, text in demos:
        with live_spinner(name, text=text, color=color):
            time.sleep(_dur(2.0, fast))
        print(f"  ✓ {text.replace('...', '')} — done\n")

    # 3. Manual start/stop with final symbol
    sp = LiveSpinner(
        "cascade",
        text="Deploying to production...",
        color="green",
        stream=sys.stderr,
    )
    sp.start()
    time.sleep(_dur(3.0, fast))
    sp.stop(symbol="✓")

    # 4. Scaled spinner (2x bigger)
    print("\n  --- 2x scaled spinner ---\n")
    with live_spinner("helix", text="Processing...", color="cyan", scale=2):
        time.sleep(_dur(3.0, fast))
    print("  ✓ Done\n")

    # 5. Show all available spinners as a gallery
    print("  --- spinner gallery ---\n")
    for name in spinners:
        with live_spinner(name, text=name, color="cyan"):
            time.sleep(_dur(1.5, fast))
        print(f"  ✓ {name}\n")

    print("  === demo complete ===\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run unicode-animations demo")
    parser.add_argument(
        "--fast",
        action="store_true",
        help="run a shorter demo (roughly 3x faster)",
    )
    args = parser.parse_args()
    run_demo(fast=args.fast)


if __name__ == "__main__":
    main()
