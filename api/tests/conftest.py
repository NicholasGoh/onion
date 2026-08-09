import pytest


@pytest.fixture
def fake_items():
    from app.data.entities import ItemData
    return [
        ItemData(name="Bluetooth Speaker", description="Portable audio"),
        ItemData(name="USB Cable", description="Type-C charging cable"),
    ]
