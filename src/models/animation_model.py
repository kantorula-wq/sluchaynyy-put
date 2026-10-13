"""Модель случайного блуждания точки на плоскости."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field


@dataclass
class RandomWalkModel:
    """Состояние и логика одномерного случайного пути в 2D.

    На каждом шаге направление получается смешиванием случайного единичного
    вектора и вектора приоритетного направления. Сила притяжения задаёт долю
    приоритетного направления в смеси (0 — равномерный случайный угол,
    1 — движение строго по приоритету).

    Attributes:
        width: Ширина области в пикселях.
        height: Высота области в пикселях.
        step_size: Длина одного шага.
        preferred_direction_deg: Угол приоритетного направления в градусах
            (0 — вправо, 90 — вверх по экрану).
        attraction_strength: Сила притяжения к приоритету, от 0.0 до 1.0.
    """

    width: float
    height: float
    step_size: float = 5.0
    preferred_direction_deg: float = 0.0
    attraction_strength: float = 0.0
    x: float = field(init=False)
    y: float = field(init=False)
    trail: list[tuple[float, float]] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        """Размещает точку в центре области."""
        self.reset()

    def reset(self) -> None:
        """Возвращает точку в центр и очищает траекторию."""
        self.x = self.width / 2.0
        self.y = self.height / 2.0
        self.trail = [(self.x, self.y)]

    def step(self) -> None:
        """Выполняет один шаг случайного блуждания."""
        dx, dy = self._sample_displacement()
        self.x += dx
        self.y += dy
        self._clamp_position()
        self.trail.append((self.x, self.y))

    def _sample_displacement(self) -> tuple[float, float]:
        """Возвращает приращение (dx, dy) для текущего шага."""
        angle_random = random.uniform(0.0, 2.0 * math.pi)
        rx = math.cos(angle_random)
        ry = math.sin(angle_random)

        angle_pref = math.radians(self.preferred_direction_deg)
        px = math.cos(angle_pref)
        # Ось Y на экране направлена вниз — инвертируем для «90° = вверх».
        py = -math.sin(angle_pref)

        strength = max(0.0, min(1.0, self.attraction_strength))
        # Линейная интерполяция направлений с последующей нормализацией.
        vx = (1.0 - strength) * rx + strength * px
        vy = (1.0 - strength) * ry + strength * py
        length = math.hypot(vx, vy)
        if length < 1e-9:
            vx, vy = px, py
        else:
            vx /= length
            vy /= length

        return vx * self.step_size, vy * self.step_size

    def _clamp_position(self) -> None:
        """Удерживает точку внутри прямоугольной области."""
        margin = 2.0
        self.x = max(margin, min(self.width - margin, self.x))
        self.y = max(margin, min(self.height - margin, self.y))
