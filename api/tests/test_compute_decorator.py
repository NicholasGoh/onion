import asyncio

from app.service.decorators import compute


class Calculator:

    def __init__(self, factor: int):
        self._factor = factor

    @compute
    def multiply(self, x: int) -> int:
        return x * self._factor


def test_sync_call_binds_self_correctly():
    calc = Calculator(factor=3)
    assert calc.multiply(4) == 12


def test_async_call_binds_self_and_matches_sync_result():
    calc = Calculator(factor=3)
    assert asyncio.run(calc.multiply.async_(4)) == 12
