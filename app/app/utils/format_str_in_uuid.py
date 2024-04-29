from typing import Any
import uuid


def format_to_str_or_nothing(data: dict[str, Any]) -> dict[str, Any]:
    """Преобразует str в UUID, если это возможно"""

    result_data = {}
    for k, v in data.items():
        try:
            v = uuid.UUID(v)

        except Exception:
            ...

        result_data.update({k: v})
    return result_data
