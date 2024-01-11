from typing import List, Dict
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Middle, Center
from textual.widgets import RichLog, Input, Header, Footer
from src.widgets.timer import TypingTimer

from src.data.sentences import Word, WordState, get_random_sentence


class TypingScreen(Screen):
    CSS_PATH = "typing.tcss"
    TITLE = "Terminal Typer"

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    paragraph: RichLog | None = None
    type_input: Input | None = None
    timer: TypingTimer | None = None

    current_index: int = 0
    current_text: List[str] = []
    check_text: Dict[int, Word]
    correct_word_count: int = 0

    def action_toggle_dark(self) -> None:
        self.app.dark = not self.app.dark

    def highlight_text(self, words: List[str]) -> None:
        for index, word in self.check_text.items():
            if index > self.current_index:
                word.state = WordState.NORMAL
            if index == self.current_index:
                self.check_text[index].state = WordState.CURRENT

            if index < self.current_index:
                if word.value == words[index]:
                    word.state = WordState.CORRECT
                else:
                    word.state = WordState.INCORRECT

    def check_correct_words(self, words: List[str]) -> None:
        for word in self.check_text.values():
            for input_word in words:
                if word.value == input_word:
                    self.correct_word_count += 1

    def on_type_input_change(self, value: str) -> None:
        assert self.type_input is not None
        assert self.timer is not None

        if not self.timer.timer_running:
            self.timer.start_timer()

        words = value.split(" ")
        self.current_index = len(words) - 1
        if self.current_index >= len(self.current_text):
            self.check_correct_words(words)
            self.generate_new_sentence()
            self.type_input.clear()

        self.highlight_text(words)
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
        self.current_text = get_random_sentence(self.app.selected_difficulty)
        self.check_text = {
            index: Word(current_word, WordState.NORMAL)
            for index, current_word in enumerate(self.current_text)
        }
        self.check_text[0].state = WordState.CURRENT
        self.update_markup()

    def on_mount(self):
        self.paragraph = self.query("#paragraph").only_one()  # type: ignore
        self.type_input = self.query("#type-input").only_one()  # type: ignore
        self.type_input.focus(scroll_visible=False)
        self.timer = self.query("#timer").only_one()  # type: ignore
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
        yield Center(
            TypingTimer(
                self.app.selected_time,  # type: ignore
                id="timer",
            ),
            Middle(richlog, input),
            id="container",
        )

    def on_typing_timer_timer_end(self) -> None:
        assert self.type_input is not None
        self.type_input.disabled = True
        words = self.type_input.value.split(" ")
        self.highlight_text(words)
        self.check_correct_words(words)
        self.app.correct_words = self.correct_word_count
        self.app.push_screen("stats")
