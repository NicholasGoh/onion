import time

from app.data.entities import Order, OrderData
from app.data.interfaces import IRepository
from app.service.crud_service import CrudService
from app.service.item_service import ItemService


class OrderService(CrudService[Order, OrderData]):

    def __init__(
        self,
        repository: IRepository[Order, OrderData],
        item_service: ItemService,
    ):
        super().__init__(repository)
        self._item_service = item_service

    def calculate_total(self, data: OrderData) -> int:
        time.sleep(1)  # mocks a pricing/tax computation
        return sum(data.quantity.get(item_id, 0) for item_id in data.item_ids)

    def create(self, data: OrderData) -> Order:
        if not data.item_ids:
            raise ValueError("Order must contain at least one item")

        missing = []
        for item_id in data.item_ids:
            if not self._item_service.get(item_id):
                missing.append(item_id)

        if missing:
            raise ValueError(f"Items not found: {missing}")

        for item_id in data.item_ids:
            if data.quantity.get(item_id, 0) < 1:
                raise ValueError(f"Quantity for item {item_id} must be at least 1")

        return super().create(data)
