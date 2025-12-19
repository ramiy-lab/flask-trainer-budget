def _ensure_positive_float(value: float, field_name: str) -> None:
    if value < 0:
        raise ValueError(f"{field_name} must be non negative, got {value}")


def _ensure_positive_int(value: int, field_name: str) -> None:
    if value < 0:
        raise ValueError(f"{field_name} must be non-negative, got {value}")
