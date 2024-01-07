from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Select, Label, Button
from textual.containers import Grid

TIME_OPTIONS = [
    ("1 Minute", 1),
    ("3 Minute", 3),
    ("5 Minute", 5),
    ("10 Minute", 10),
]

DIFFICULTY_OPTIONS = [
    ("Easy", "easy"),
    ("Medium", "medium"),
    ("Hard", "hard"),
]


class InitialScreen(Screen):
    CSS_PATH = "initial.tcss"

    def compose(self) -> ComposeResult:
        container = Grid(
            Label(" Select time: "),
            Select(
                TIME_OPTIONS,
                prompt="Select time",
                allow_blank=False,
                value=1,
                id="time-select",
            ),
            Label(" Select difficulty: "),
            Select(
                DIFFICULTY_OPTIONS,
                prompt="Select difficulty",
                allow_blank=False,
                value="easy",
                id="difficulty-select",
            ),
            Button(
                "Start",
                variant="primary",
                id="start-button",
            ),
            id="initial-screen",
        )
        container.border_title = "Terminal Typer"
        yield container

    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start-button":
            self.app.push_screen("typing")