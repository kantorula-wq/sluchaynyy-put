"""Юнит-тесты модели случайного блуждания."""

import math
import unittest
from unittest.mock import patch

from src.models.animation_model import RandomWalkModel


class RandomWalkModelTests(unittest.TestCase):
    """Проверки центра старта, шага и смещения по приоритету."""

    def test_starts_at_center(self) -> None:
        model = RandomWalkModel(width=200.0, height=100.0)
        self.assertEqual(model.x, 100.0)
        self.assertEqual(model.y, 50.0)
        self.assertEqual(len(model.trail), 1)

    def test_reset_clears_trail(self) -> None:
        model = RandomWalkModel(width=100.0, height=100.0, step_size=10.0)
        with patch("src.models.animation_model.random.uniform", return_value=0.0):
            model.step()
        self.assertGreater(len(model.trail), 1)
        model.reset()
        self.assertEqual(len(model.trail), 1)
        self.assertEqual(model.x, 50.0)
        self.assertEqual(model.y, 50.0)

    def test_step_size_affects_displacement(self) -> None:
        model = RandomWalkModel(
            width=400.0,
            height=400.0,
            step_size=20.0,
            attraction_strength=1.0,
            preferred_direction_deg=0.0,
        )
        with patch("src.models.animation_model.random.uniform", return_value=0.0):
            x0, y0 = model.x, model.y
            model.step()
        self.assertAlmostEqual(model.x - x0, 20.0, places=5)
        self.assertAlmostEqual(model.y - y0, 0.0, places=5)

    def test_full_attraction_moves_up_at_90_degrees(self) -> None:
        model = RandomWalkModel(
            width=400.0,
            height=400.0,
            step_size=10.0,
            attraction_strength=1.0,
            preferred_direction_deg=90.0,
        )
        with patch("src.models.animation_model.random.uniform", return_value=0.0):
            y0 = model.y
            model.step()
        self.assertAlmostEqual(model.y, y0 - 10.0, places=5)

    def test_displacement_vector_is_normalized(self) -> None:
        model = RandomWalkModel(
            width=400.0,
            height=400.0,
            step_size=7.0,
            attraction_strength=0.5,
            preferred_direction_deg=45.0,
        )
        with patch(
            "src.models.animation_model.random.uniform",
            return_value=math.pi / 4,
        ):
            x0, y0 = model.x, model.y
            model.step()
        dist = math.hypot(model.x - x0, model.y - y0)
        self.assertAlmostEqual(dist, 7.0, places=5)


if __name__ == "__main__":
    unittest.main()
