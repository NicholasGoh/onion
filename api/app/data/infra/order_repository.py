from typing import Optional

from sqlmodel import Column, Field, Session, SQLModel, select
from sqlalchemy import JSON

from app.data.entities import Order, OrderData
from app.data.interfaces import IRepository


class OrderModel(SQLModel, table=True):
    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    item_ids: list[int] = Field(sa_column=Column(JSON))
    quantity: dict[int, int] = Field(sa_column=Column(JSON))
    status: str = "pending"

    def to_entity(self) -> Order:
        return Order(
            id=self.id or 0,
            item_ids=self.item_ids,
            quantity=self.quantity,
            status=self.status,
        )


class OrderRepository(IRepository[Order, OrderData]):

    def __init__(self, session: Session):
        self.session = session

    def create(self, data: OrderData) -> Order:
        model = OrderModel(
            item_ids=data.item_ids,
            quantity=data.quantity,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model.to_entity()

    def get_by_id(self, id: int) -> Order | None:
        model = self.session.get(OrderModel, id)
        return model.to_entity() if model else None

    def get_all(self) -> list[Order]:
        statement = select(OrderModel)
        results = self.session.exec(statement)
        return [model.to_entity() for model in results]

    def delete(self, id: int) -> bool:
        model = self.session.get(OrderModel, id)
        if not model:
            return False
        self.session.delete(model)
        self.session.commit()
        return True
