"""Главное окно и цикл анимации случайного пути."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from src.models.animation_model import RandomWalkModel
from src.renderers.renderer import RandomWalkRenderer
from src.widgets.controls import ControlPanel


class App:
    """Окно приложения с холстом, панелью управления и таймером анимации."""

    CANVAS_WIDTH = 640
    CANVAS_HEIGHT = 480
    TICK_MS = 30

    def __init__(self) -> None:
        """Инициализирует модель, интерфейс и запускает цикл обновления."""
        self._root = tk.Tk()
        self._root.title("Случайный путь — Кантор Ульяна")
        self._root.minsize(720, 560)

        self._model = RandomWalkModel(
            width=float(self.CANVAS_WIDTH),
            height=float(self.CANVAS_HEIGHT),
        )
        self._paused = False
        self._after_id: str | None = None

        self._build_ui()
        self._bind_keys()
        self._schedule_tick()

    def _build_ui(self) -> None:
        """Собирает холст и панель управления."""
        main = ttk.Frame(self._root, padding=8)
        main.pack(fill=tk.BOTH, expand=True)

        canvas_frame = ttk.Frame(main)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self._canvas = tk.Canvas(
            canvas_frame,
            width=self.CANVAS_WIDTH,
            height=self.CANVAS_HEIGHT,
            bg="#1e1e2e",
            highlightthickness=1,
            highlightbackground="#444",
        )
        self._canvas.pack()

        self._renderer = RandomWalkRenderer(self._canvas)
        self._renderer.draw(self._model)

        self._controls = ControlPanel(
            main,
            on_step_change=self._set_step_size,
            on_direction_change=self._set_direction,
            on_attraction_change=self._set_attraction,
            on_reset=self._reset,
            on_toggle_pause=self._toggle_pause,
        )
        self._controls.pack(fill=tk.X, pady=(8, 0))

    def _bind_keys(self) -> None:
        """Назначает горячие клавиши Space (пауза) и R (сброс)."""
        self._root.bind("<space>", lambda _event: self._toggle_pause())
        self._root.bind("<r>", lambda _event: self._reset())
        self._root.bind("<R>", lambda _event: self._reset())

    def _set_step_size(self, value: float) -> None:
        self._model.step_size = value

    def _set_direction(self, value: float) -> None:
        self._model.preferred_direction_deg = value

    def _set_attraction(self, value: float) -> None:
        self._model.attraction_strength = value

    def _reset(self) -> None:
        self._model.reset()
        self._renderer.draw(self._model)

    def _toggle_pause(self) -> None:
        self._paused = not self._paused
        self._controls.set_paused(self._paused)

    def _schedule_tick(self) -> None:
        self._after_id = self._root.after(self.TICK_MS, self._on_tick)

    def _on_tick(self) -> None:
        if not self._paused:
            self._model.step()
            self._renderer.draw(self._model)
        self._schedule_tick()

    def run(self) -> None:
        """Запускает главный цикл tkinter."""
        self._root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._root.mainloop()

    def _on_close(self) -> None:
        if self._after_id is not None:
            self._root.after_cancel(self._after_id)
        self._root.destroy()
