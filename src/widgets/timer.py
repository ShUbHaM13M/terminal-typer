from textual.widgets import Static
from textual.message import Message
from textual.reactive import reactive
from textual.timer import Timer


class TypingTimer(Static):
    time = reactive(0.0)
    timer_running: bool = False
    update_timer: Timer | None = None

    class TimerEnd(Message):
        pass

    def __init__(self, duration_in_min: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.start_time = duration_in_min * 60

    def on_mount(self) -> None:
        self.time = self.start_time
        minutes, seconds = divmod(self.time, 60)
        _, minutes = divmod(minutes, 60)
        self.renderable = f"Time: {minutes:02.0f}:{seconds:02.0f}"
        self.update_timer = self.set_interval(1, self.update_time, pause=True)

    def start_timer(self) -> None:
        assert self.update_timer is not None
        self.timer_running = True
        self.update_timer.resume()

    def update_time(self) -> None:
        self.start_time -= 1
        self.time = self.start_time

    def watch_time(self, time: float) -> None:
        if time == 0 and self.update_timer:
            self.update(f"Time: 00:00")
            self.post_message(self.TimerEnd())
            self.update_timer.stop()
            return

        minutes, seconds = divmod(time, 60)
        _, minutes = divmod(minutes, 60)
        if self.timer_running:
            self.update(f"Time: {minutes:02.0f}:{seconds:02.0f}")
