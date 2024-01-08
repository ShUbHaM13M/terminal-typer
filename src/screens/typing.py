from typing import List, Dict
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Middle
from textual.widgets import RichLog, Input, Header, Footer

from src.data.sentences import Word, WordState, get_random_sentence


class TypingScreen(Screen):
    CSS_PATH = "typing.tcss"
    TITLE = "Terminal Typer"

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    paragraph: RichLog | None = None
    type_input: Input | None = None
    current_index: int = 0
    current_text: List[str] = []
    check_text: Dict[int, Word]

    def action_toggle_dark(self) -> None:
        self.app.dark = not self.app.dark

    def on_type_input_change(self, value: str) -> None:
        assert self.type_input is not None
        words = value.split(" ")
        self.current_index = len(words) - 1
        if self.current_index >= len(self.current_text):
            self.generate_new_sentence()
            self.type_input.clear()

        # TODO: Optimization: prevent looping over the words which are ahead of the current index
        for index, word in self.check_text.items():
            word.state = WordState.NORMAL
            if index == self.current_index:
                self.check_text[index].state = WordState.CURRENT

            if index < self.current_index:
                if word.value == words[index]:
                    word.state = WordState.CORRECT
                else:
                    word.state = WordState.INCORRECT

        self.update_markup()

    def on_input_changed(self, event: Input.Changed):
        if event.input.id == "type-input":
            self.on_type_input_change(event.value)

    def update_markup(self):
        assert self.paragraph is not None
        markup = ""
        for current in self.check_text.values():
            word = current.value
            match current.state:
                case WordState.CURRENT:
                    word = f"[underline blue]{word}[/underline blue]"
                case WordState.CORRECT:
                    word = f"[bold green]{word}[/bold green]"
                case WordState.INCORRECT:
                    word = f"[bold red]{word}[/bold red]"
                case _:
                    pass

            markup += " " + word

        self.paragraph.clear()
        self.paragraph.write(markup)

    def generate_new_sentence(self):
        self.current_text = get_random_sentence().strip().split()
        self.check_text = {
            index: Word(current_word, WordState.NORMAL)
            for index, current_word in enumerate(self.current_text)
        }
        self.check_text[0].state = WordState.CURRENT
        self.update_markup()

    def on_mount(self):
        self.paragraph = self.query_one(RichLog)
        self.type_input = self.query_one(Input)
        self.generate_new_sentence()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        richlog = RichLog(
            markup=True,
            highlight=True,
            auto_scroll=False,
            id="paragraph",
            wrap=True,
        )
        input = Input(
            type="text",
            placeholder="Type...",
            id="type-input",
        )
        yield Middle(richlog, input)
