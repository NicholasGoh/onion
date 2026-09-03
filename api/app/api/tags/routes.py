from dependency_injector.wiring import Provide

from app.api.crud_router import add_get_by_id, make_crud_router
from app.api.tags.contracts import TagCreate, TagRead
from app.container import Container

router = make_crud_router(
    prefix="/tags",
    tag="tags",
    create_dto=TagCreate,
    read_dto=TagRead,
    service_provider=Provide[Container.tag_service],
)

add_get_by_id(
    router,
    tag="tags",
    read_dto=TagRead,
    service_provider=Provide[Container.tag_service],
)
