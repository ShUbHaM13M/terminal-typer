from textual.app import App

from src.screens.initial import InitialScreen
from src.screens.typing import TypingScreen


class TerminalTyper(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    TITLE = "Terminal Typer"
    CSS_PATH = "styles.tcss"
    SCREENS = {
        "initial": InitialScreen(),
        "typing": TypingScreen(),
    }

    selected_time: int = 1
    selected_difficulty: str

    def on_mount(self) -> None:
        self.push_screen("initial")

    def action_toggle_dark(self) -> None:
        self.log(self.selected_difficulty)
        self.dark = not self.dark
