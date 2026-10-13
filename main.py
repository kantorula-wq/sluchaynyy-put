"""Точка входа приложения «Случайный путь»."""

from src.app import App


def main() -> None:
    """Запускает главное окно приложения."""
    app = App()
    app.run()


if __name__ == "__main__":
    main()
