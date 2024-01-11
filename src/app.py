from textual.app import App
from src.screens import InitialScreen, TypingScreen, StatsScreen


class TerminalTyper(App):
    DEBUG = True
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    TITLE = "Terminal Typer"
    CSS_PATH = "styles.tcss"

    SCREENS = {
        "initial": InitialScreen(),
        "typing": TypingScreen(),
        "stats": StatsScreen(),
    }

    selected_time: int = 1
    selected_difficulty: str = "easy"
    correct_words: int = 0

    def on_mount(self) -> None:
        self.push_screen("initial")

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark
