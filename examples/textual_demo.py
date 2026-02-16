"""Textual TUI demo showcasing unicode-animations spinners."""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Footer, Header, Label, Static

from unicode_animations import scale_spinner, spinners

COLORS = [
    "cyan",
    "green",
    "yellow",
    "magenta",
    "red",
    "blue",
    "white",
    "cyan",
    "green",
    "yellow",
    "magenta",
    "red",
    "blue",
    "white",
    "cyan",
    "green",
    "yellow",
    "magenta",
]

SPINNER_NAMES = list(spinners.keys())


class SpinnerWidget(Static):
    """Animates a single braille spinner."""

    frame_idx: reactive[int] = reactive(0)

    def __init__(self, spinner_name: str, color: str, scale: int = 1) -> None:
        super().__init__()
        sp = spinners[spinner_name]
        if scale > 1:
            sp = scale_spinner(sp, scale)
        self._frames = sp.frames
        self._interval = sp.interval / 1000
        self._spinner_name = spinner_name
        self._color = color

    def on_mount(self) -> None:
        self.set_interval(self._interval, self._advance)

    def _advance(self) -> None:
        self.frame_idx += 1

    def watch_frame_idx(self) -> None:
        frame = self._frames[self.frame_idx % len(self._frames)]
        self.update(f"[{self._color}]{frame}[/]")


class SpinnerCard(Static):
    """A card containing a spinner and its name label."""

    DEFAULT_CSS = """
    SpinnerCard {
        width: 1fr;
        height: auto;
        padding: 1 2;
        margin: 1;
        border: round $surface-lighten-2;
        layout: vertical;
        content-align: center middle;
    }

    SpinnerCard .spinner-frame {
        width: 100%;
        content-align: center middle;
        height: auto;
        min-height: 3;
    }

    SpinnerCard .spinner-label {
        width: 100%;
        text-align: center;
        color: $text-muted;
        margin-top: 1;
    }
    """

    def __init__(self, spinner_name: str, color: str, scale: int = 1) -> None:
        super().__init__()
        self._spinner_name = spinner_name
        self._color = color
        self._scale = scale

    def compose(self) -> ComposeResult:
        yield SpinnerWidget(
            self._spinner_name,
            self._color,
            scale=self._scale,
        ).add_class("spinner-frame")
        yield Label(self._spinner_name).add_class("spinner-label")


class SpinnerGallery(App):
    """A gallery of all unicode-animations spinners."""

    CSS = """
    Screen {
        background: $surface;
    }

    #gallery {
        padding: 1 2;
    }

    .row {
        height: auto;
        width: 100%;
    }

    #scaled-section {
        margin-top: 2;
        padding: 1 2;
    }

    #scaled-header {
        text-align: center;
        width: 100%;
        margin-bottom: 1;
        text-style: bold;
        color: $text;
    }

    .scaled-row {
        height: auto;
        width: 100%;
    }
    """

    TITLE = "unicode-animations"
    SUB_TITLE = f"{len(SPINNER_NAMES)} braille spinners"

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with VerticalScroll(id="gallery"):
            # Normal scale: 3 per row
            for i in range(0, len(SPINNER_NAMES), 3):
                with Horizontal(classes="row"):
                    for j in range(3):
                        if i + j < len(SPINNER_NAMES):
                            name = SPINNER_NAMES[i + j]
                            color = COLORS[(i + j) % len(COLORS)]
                            yield SpinnerCard(name, color)

            # Scaled section
            yield Label("── 2x scaled ──", id="scaled-header")
            scaled_picks = ["helix", "dna", "rain"]
            with Horizontal(classes="scaled-row"):
                for name in scaled_picks:
                    color = COLORS[SPINNER_NAMES.index(name) % len(COLORS)]
                    yield SpinnerCard(name, color, scale=2)

        yield Footer()


if __name__ == "__main__":
    SpinnerGallery().run()
