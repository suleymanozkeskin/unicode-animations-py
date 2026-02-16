"""LiveSpinner — threaded background spinner for CLI apps."""

from __future__ import annotations

import sys
import threading
from typing import IO, Union

from .braille import BrailleSpinnerName, Spinner, scale_spinner, spinners

_COLORS: dict[str, str] = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}
_RESET = "\033[0m"


class LiveSpinner:
    """Threaded background spinner that renders to a terminal stream.

    Usage::

        with LiveSpinner("helix", text="Loading...", color="cyan"):
            do_work()
    """

    def __init__(
        self,
        name_or_spinner: Union[BrailleSpinnerName, Spinner],
        text: str = "",
        color: str | None = None,
        stream: IO[str] | None = None,
        scale: int = 1,
    ) -> None:
        if isinstance(name_or_spinner, Spinner):
            spinner = name_or_spinner
        else:
            spinner = spinners[name_or_spinner]

        self._spinner = scale_spinner(spinner, scale) if scale > 1 else spinner
        self._text = text
        self._color = color
        self._stream: IO[str] = stream if stream is not None else sys.stderr
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._last_rendered_lines = 0

    @property
    def _is_tty(self) -> bool:
        return hasattr(self._stream, "isatty") and self._stream.isatty()

    def _format_frame(self, frame: str) -> str:
        lines = frame.splitlines() or [""]
        if self._color and self._is_tty:
            code = _COLORS.get(self._color, "")
            if code:
                lines = [f"{code}{line}{_RESET}" for line in lines]
        if self._text:
            lines[0] = f"{lines[0]} {self._text}" if lines[0] else self._text
        return "\n".join(lines)

    def _clear_rendered(self) -> None:
        if self._last_rendered_lines <= 0:
            return
        write = self._stream.write
        for i in range(self._last_rendered_lines):
            write("\r\033[2K")
            if i < self._last_rendered_lines - 1:
                write("\033[1A")
        self._last_rendered_lines = 0

    def _run(self) -> None:
        frames = self._spinner.frames
        interval = self._spinner.interval / 1000
        idx = 0
        write = self._stream.write
        flush = self._stream.flush
        # Hide cursor
        write("\033[?25l")
        flush()
        while not self._stop_event.is_set():
            self._clear_rendered()
            rendered = self._format_frame(frames[idx % len(frames)])
            write(rendered)
            self._last_rendered_lines = len(rendered.splitlines()) or 1
            flush()
            idx += 1
            self._stop_event.wait(interval)

    def start(self) -> None:
        """Start the spinner animation."""
        if not self._is_tty:
            # Non-TTY fallback: just print the text once
            if self._text:
                self._stream.write(self._text + "\n")
                self._stream.flush()
            return
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._last_rendered_lines = 0
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self, symbol: str = "") -> None:
        """Stop the spinner and optionally show a final symbol."""
        if self._thread is None:
            return
        self._stop_event.set()
        self._thread.join()
        self._thread = None
        # Clear line and show final symbol
        write = self._stream.write
        flush = self._stream.flush
        self._clear_rendered()
        if symbol:
            suffix = f" {self._text}" if self._text else ""
            write(f"{symbol}{suffix}\n")
        # Restore cursor
        write("\033[?25h")
        flush()

    def __enter__(self) -> LiveSpinner:
        self.start()
        return self

    def __exit__(self, *_: object) -> None:
        self.stop()


def live_spinner(
    name_or_spinner: Union[BrailleSpinnerName, Spinner],
    text: str = "",
    color: str | None = None,
    stream: IO[str] | None = None,
    scale: int = 1,
) -> LiveSpinner:
    """Convenience function that returns a :class:`LiveSpinner`."""
    return LiveSpinner(
        name_or_spinner, text=text, color=color, stream=stream, scale=scale
    )
