from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from app.api.orders.contracts import OrderCreate, OrderRead
from app.container import Container
from app.service.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderRead)
@inject
def create_order(
    order: OrderCreate,
    service: OrderService = Depends(Provide[Container.order_service]),
):
    try:
        domain_order = service.create(order.to_entity())
        return OrderRead.from_entity(domain_order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{order_id}", response_model=OrderRead)
@inject
def get_order(
    order_id: int,
    service: OrderService = Depends(Provide[Container.order_service]),
):
    domain_order = service.get(order_id)
    if not domain_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderRead.from_entity(domain_order)


@router.get("/", response_model=list[OrderRead])
@inject
def get_orders(
    service: OrderService = Depends(Provide[Container.order_service]),
):
    domain_orders = service.get_all()
    return [OrderRead.from_entity(order) for order in domain_orders]
