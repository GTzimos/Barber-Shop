from __future__ import annotations

from typing import Callable


def logout(current_window, on_logout: Callable[[], None] | None = None) -> None:
    current_window.close()
    if on_logout:
        on_logout()
