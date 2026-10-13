"""Отрисовка траектории и текущей позиции на tkinter Canvas."""

from __future__ import annotations

import tkinter as tk

from src.models.animation_model import RandomWalkModel


class RandomWalkRenderer:
    """Рисует след случайного пути и текущую точку."""

    TRAIL_COLOR = "#4a90d9"
    POINT_COLOR = "#e74c3c"
    POINT_RADIUS = 4

    def __init__(self, canvas: tk.Canvas) -> None:
        """Сохраняет ссылку на холст для отрисовки.

        Args:
            canvas: Виджет Canvas, на котором рисуется симуляция.
        """
        self._canvas = canvas
        self._trail_item: int | None = None
        self._point_item: int | None = None

    def draw(self, model: RandomWalkModel) -> None:
        """Обновляет линию траектории и маркер точки.

        Args:
            model: Модель с актуальными координатами и историей шагов.
        """
        if self._trail_item is not None:
            self._canvas.delete(self._trail_item)
        if self._point_item is not None:
            self._canvas.delete(self._point_item)

        if len(model.trail) >= 2:
            flat = [coord for point in model.trail for coord in point]
            self._trail_item = self._canvas.create_line(
                *flat,
                fill=self.TRAIL_COLOR,
                width=2,
                smooth=False,
            )
        else:
            self._trail_item = None

        x, y = model.x, model.y
        r = self.POINT_RADIUS
        self._point_item = self._canvas.create_oval(
            x - r,
            y - r,
            x + r,
            y + r,
            fill=self.POINT_COLOR,
            outline="",
        )

    def clear(self) -> None:
        """Удаляет все созданные элементы с холста."""
        if self._trail_item is not None:
            self._canvas.delete(self._trail_item)
            self._trail_item = None
        if self._point_item is not None:
            self._canvas.delete(self._point_item)
            self._point_item = None
