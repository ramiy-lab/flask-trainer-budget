import pytest

from services.validators._common import (
    _ensure_positive_float,
    _ensure_positive_int,
)


@pytest.mark.parametrize(
    "value",
    [0.0, 1.0, 10.5],
)
def test_ensure_positive_float_valid(value: float) -> None:
    _ensure_positive_float(value, "test_field")


@pytest.mark.parametrize(
    "value",
    [-0.1, -1.0],
)
def test_ensure_positive_float_invalid(value: float) -> None:
    with pytest.raises(ValueError, match="test_field"):
        _ensure_positive_float(value, "test_field")


@pytest.mark.parametrize(
    "value",
    [0, 1, 10],
)
def test_ensure_positive_int_valid(value: int) -> None:
    _ensure_positive_int(value, "test_field")


@pytest.mark.parametrize(
    "value",
    [-1, -10],
)
def test_ensure_positive_int_invalid(value: int) -> None:
    with pytest.raises(ValueError, match="test_field"):
        _ensure_positive_int(value, "test_field")
