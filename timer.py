"""タイマー（30秒〜5分、30秒刻みで設定可能）"""

import tkinter as tk
import winsound
from tkinter import font

DEFAULT_DURATION = 30
PRESET_DURATIONS = list(range(30, 301, 30))  # 30秒, 1分, ... 5分


def _preset_label(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}秒"
    minutes = seconds // 60
    remainder = seconds % 60
    if remainder == 0:
        return f"{minutes}分"
    return f"{minutes}:{remainder:02d}"


class TimerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("タイマー")
        self.root.geometry("520x380")
        self.root.resizable(False, False)

        self.duration = DEFAULT_DURATION
        self.remaining = DEFAULT_DURATION
        self.running = False
        self.after_id: str | None = None

        time_font = font.Font(family="Helvetica", size=56, weight="bold")
        self.time_label = tk.Label(root, text=self._format_time(), font=time_font)
        self.time_label.pack(pady=24)

        preset_frame = tk.Frame(root)
        preset_frame.pack(pady=8)

        for index, seconds in enumerate(PRESET_DURATIONS):
            row = index // 5
            col = index % 5
            tk.Button(
                preset_frame,
                text=_preset_label(seconds),
                width=7,
                command=lambda s=seconds: self.set_duration(s),
            ).grid(row=row, column=col, padx=4, pady=4)

        control_frame = tk.Frame(root)
        control_frame.pack(pady=16)

        tk.Button(control_frame, text="スタート", width=10, command=self.start).grid(
            row=0, column=0, padx=10
        )
        tk.Button(control_frame, text="ストップ", width=10, command=self.stop).grid(
            row=0, column=1, padx=10
        )
        tk.Button(control_frame, text="リセット", width=10, command=self.reset).grid(
            row=0, column=2, padx=10
        )

    def _format_time(self) -> str:
        minutes = self.remaining // 60
        seconds = self.remaining % 60
        return f"{minutes:02d}:{seconds:02d}"

    def _update_display(self) -> None:
        self.time_label.config(text=self._format_time())

    def _play_alarm(self) -> None:
        for _ in range(3):
            winsound.Beep(880, 300)

    def set_duration(self, seconds: int) -> None:
        self.stop()
        self.duration = seconds
        self.remaining = seconds
        self.time_label.config(text=self._format_time(), fg="black")

    def _tick(self) -> None:
        if not self.running:
            return

        if self.remaining > 0:
            self.remaining -= 1
            self._update_display()

        if self.remaining == 0:
            self.running = False
            self.time_label.config(fg="red")
            self._play_alarm()
            return

        self.after_id = self.root.after(1000, self._tick)

    def start(self) -> None:
        if self.remaining > 0 and not self.running:
            self.running = True
            self.time_label.config(fg="black")
            self._tick()

    def stop(self) -> None:
        self.running = False
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def reset(self) -> None:
        self.stop()
        self.remaining = self.duration
        self.time_label.config(text=self._format_time(), fg="black")


def main() -> None:
    root = tk.Tk()
    TimerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
