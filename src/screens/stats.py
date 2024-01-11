from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Placeholder, Label
from textual.screen import Screen


class StatsScreen(Screen):
    CSS_PATH = "./stats.tcss"

    def compose(self) -> ComposeResult:
        container = Container(
            Label(
                f"Time: {self.app.selected_time}\n",
                id="timer-label",
            ),
            Label(
                f"Correct word count: {self.app.correct_words}",
                id="correct-label",
            ),
            id="container",
        )
        container.border_title = "Stats"
        yield container
