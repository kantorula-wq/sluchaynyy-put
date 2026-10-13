"""Панель слайдеров для параметров симуляции."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable


class ControlPanel(ttk.Frame):
    """Слайдеры величины шага, направления и силы притяжения."""

    def __init__(
        self,
        master: tk.Misc,
        on_step_change: Callable[[float], None],
        on_direction_change: Callable[[float], None],
        on_attraction_change: Callable[[float], None],
        on_reset: Callable[[], None],
        on_toggle_pause: Callable[[], None],
        **kwargs: object,
    ) -> None:
        """Создаёт элементы управления и связывает их с колбэками.

        Args:
            master: Родительский виджет.
            on_step_change: Вызывается при изменении величины шага.
            on_direction_change: Вызывается при изменении угла направления.
            on_attraction_change: Вызывается при изменении силы притяжения.
            on_reset: Сброс симуляции.
            on_toggle_pause: Пауза / продолжение.
        """
        super().__init__(master, **kwargs)
        self._on_toggle_pause = on_toggle_pause
        self._pause_button: ttk.Button

        self._build_step_slider(on_step_change)
        self._build_direction_slider(on_direction_change)
        self._build_attraction_slider(on_attraction_change)

        button_row = ttk.Frame(self)
        button_row.pack(fill=tk.X, pady=8)
        ttk.Button(button_row, text="Сброс", command=on_reset).pack(
            side=tk.LEFT, padx=4
        )
        self._pause_button = ttk.Button(
            button_row,
            text="Пауза",
            command=self._handle_pause_click,
        )
        self._pause_button.pack(side=tk.LEFT, padx=4)

    def set_paused(self, paused: bool) -> None:
        """Обновляет подпись кнопки паузы."""
        self._pause_button.configure(text="Продолжить" if paused else "Пауза")

    def _handle_pause_click(self) -> None:
        self._on_toggle_pause()

    def _build_step_slider(self, callback: Callable[[float], None]) -> None:
        row = ttk.Frame(self)
        row.pack(fill=tk.X, pady=4)
        ttk.Label(row, text="Величина шага", width=22).pack(side=tk.LEFT)
        var = tk.DoubleVar(value=5.0)
        scale = ttk.Scale(
            row,
            from_=1.0,
            to=30.0,
            variable=var,
            orient=tk.HORIZONTAL,
            command=lambda _: callback(var.get()),
        )
        scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
        ttk.Label(row, textvariable=var, width=5).pack(side=tk.LEFT)

    def _build_direction_slider(self, callback: Callable[[float], None]) -> None:
        row = ttk.Frame(self)
        row.pack(fill=tk.X, pady=4)
        ttk.Label(row, text="Приоритетное направление (°)", width=22).pack(
            side=tk.LEFT
        )
        var = tk.DoubleVar(value=0.0)
        scale = ttk.Scale(
            row,
            from_=0.0,
            to=360.0,
            variable=var,
            orient=tk.HORIZONTAL,
            command=lambda _: callback(var.get()),
        )
        scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
        ttk.Label(row, textvariable=var, width=5).pack(side=tk.LEFT)

    def _build_attraction_slider(self, callback: Callable[[float], None]) -> None:
        row = ttk.Frame(self)
        row.pack(fill=tk.X, pady=4)
        ttk.Label(row, text="Сила притяжения", width=22).pack(side=tk.LEFT)
        var = tk.DoubleVar(value=0.0)
        scale = ttk.Scale(
            row,
            from_=0.0,
            to=1.0,
            variable=var,
            orient=tk.HORIZONTAL,
            command=lambda _: callback(var.get()),
        )
        scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
        ttk.Label(row, textvariable=var, width=5).pack(side=tk.LEFT)
