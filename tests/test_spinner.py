import io

from unicode_animations.braille import Spinner
from unicode_animations.spinner import LiveSpinner, live_spinner, _COLORS, _RESET


class TestLiveSpinnerStartStop:
    def test_starts_and_stops_cleanly(self):
        stream = io.StringIO()
        sp = LiveSpinner("braille", text="testing", stream=stream)
        # Non-TTY stream — should not spawn a thread
        sp.start()
        assert sp._thread is None
        sp.stop()

    def test_context_manager(self):
        stream = io.StringIO()
        with LiveSpinner("braille", text="ctx", stream=stream) as sp:
            assert isinstance(sp, LiveSpinner)
        # After exit, thread should be None
        assert sp._thread is None


class TestNonTTYFallback:
    def test_prints_text_once(self):
        stream = io.StringIO()
        sp = LiveSpinner("braille", text="Loading...", stream=stream)
        sp.start()
        sp.stop()
        assert stream.getvalue() == "Loading...\n"

    def test_no_text_prints_nothing(self):
        stream = io.StringIO()
        sp = LiveSpinner("braille", stream=stream)
        sp.start()
        sp.stop()
        assert stream.getvalue() == ""


class TestColorWrapping:
    def test_no_color_no_wrapping(self):
        sp = LiveSpinner("braille", stream=io.StringIO())
        frame = sp._format_frame("⠋")
        assert "\033[" not in frame
        assert "⠋" in frame

    def test_color_ignored_on_non_tty(self):
        sp = LiveSpinner("braille", color="cyan", stream=io.StringIO())
        frame = sp._format_frame("⠋")
        # StringIO is not a TTY, so no ANSI codes
        assert _COLORS["cyan"] not in frame

    def test_color_applied_on_tty(self):
        class FakeTTY(io.StringIO):
            def isatty(self) -> bool:
                return True

        sp = LiveSpinner("braille", color="cyan", stream=FakeTTY())
        frame = sp._format_frame("⠋")
        assert frame.startswith(_COLORS["cyan"])
        assert _RESET in frame

    def test_invalid_color_no_wrapping(self):
        class FakeTTY(io.StringIO):
            def isatty(self) -> bool:
                return True

        sp = LiveSpinner("braille", color="nope", stream=FakeTTY())
        frame = sp._format_frame("⠋")
        assert "\033[" not in frame


class TestLiveSpinnerConvenience:
    def test_returns_live_spinner(self):
        sp = live_spinner("helix", text="hi", color="green", stream=io.StringIO())
        assert isinstance(sp, LiveSpinner)

    def test_usable_as_context_manager(self):
        stream = io.StringIO()
        with live_spinner("helix", text="work", stream=stream):
            pass
        assert "work" in stream.getvalue()


class TestCustomSpinnerInstance:
    def test_accepts_spinner_instance(self):
        custom = Spinner(frames=("A", "B", "C"), interval=100)
        stream = io.StringIO()
        sp = LiveSpinner(custom, text="custom", stream=stream)
        assert sp._spinner is custom
        sp.start()
        sp.stop()
        assert "custom" in stream.getvalue()

    def test_custom_spinner_context_manager(self):
        custom = Spinner(frames=("X", "Y"), interval=50)
        stream = io.StringIO()
        with LiveSpinner(custom, stream=stream, text="go"):
            pass
        assert "go" in stream.getvalue()


class TestTextFormatting:
    def test_frame_with_text(self):
        sp = LiveSpinner("braille", text="Loading", stream=io.StringIO())
        frame = sp._format_frame("⠋")
        assert frame == "⠋ Loading"

    def test_frame_without_text(self):
        sp = LiveSpinner("braille", stream=io.StringIO())
        frame = sp._format_frame("⠋")
        assert frame == "⠋"

    def test_multiline_frame_puts_text_on_first_line(self):
        sp = LiveSpinner("braille", text="Loading", stream=io.StringIO())
        frame = sp._format_frame("⠋\n⠙")
        assert frame == "⠋ Loading\n⠙"


class TestScaleParam:
    def test_scale_1_default(self):
        from unicode_animations.braille import spinners
        sp = LiveSpinner("braille", stream=io.StringIO())
        assert sp._spinner is spinners["braille"]

    def test_scale_2_produces_wider_frames(self):
        from unicode_animations.braille import spinners
        sp = LiveSpinner("helix", stream=io.StringIO(), scale=2)
        original_width = len(spinners["helix"].frames[0])
        scaled_width = len(sp._spinner.frames[0])
        assert scaled_width > original_width

    def test_live_spinner_convenience_scale(self):
        from unicode_animations.braille import spinners
        sp = live_spinner("helix", stream=io.StringIO(), scale=2)
        original_width = len(spinners["helix"].frames[0])
        assert len(sp._spinner.frames[0]) > original_width

    def test_scale_2_produces_multiline_frames(self):
        sp = LiveSpinner("helix", stream=io.StringIO(), scale=2)
        assert "\n" in sp._spinner.frames[0]


class TestTTYSpinner:
    def test_thread_starts_on_tty(self):
        class FakeTTY(io.StringIO):
            def isatty(self) -> bool:
                return True

        stream = FakeTTY()
        sp = LiveSpinner("braille", text="tty", stream=stream)
        sp.start()
        assert sp._thread is not None
        assert sp._thread.is_alive()
        sp.stop()
        assert sp._thread is None

    def test_stop_with_symbol(self):
        class FakeTTY(io.StringIO):
            def isatty(self) -> bool:
                return True

        stream = FakeTTY()
        sp = LiveSpinner("braille", text="done", stream=stream)
        sp.start()
        sp.stop(symbol="✓")
        output = stream.getvalue()
        assert "✓" in output
        assert "done" in output

    def test_can_restart_after_stop(self):
        class FakeTTY(io.StringIO):
            def isatty(self) -> bool:
                return True

        stream = FakeTTY()
        sp = LiveSpinner("braille", text="again", stream=stream)
        sp.start()
        sp.stop()
        sp.start()
        assert sp._thread is not None
        assert sp._thread.is_alive()
        sp.stop()
