from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from app.api.tag_contracts import TagCreate, TagRead
from app.container import Container
from app.data.entities import Tag, TagData
from app.service.crud_service import CrudService

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/", response_model=TagRead)
@inject
def create_tag(
    tag: TagCreate,
    service: CrudService[Tag, TagData] = Depends(Provide[Container.tag_service]),
):
    domain_tag = service.create(tag.to_entity())
    return TagRead.from_entity(domain_tag)


@router.get("/{tag_id}", response_model=TagRead)
@inject
def get_tag(
    tag_id: int,
    service: CrudService[Tag, TagData] = Depends(Provide[Container.tag_service]),
):
    domain_tag = service.get(tag_id)
    if not domain_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return TagRead.from_entity(domain_tag)


@router.get("/", response_model=list[TagRead])
@inject
def get_tags(
    service: CrudService[Tag, TagData] = Depends(Provide[Container.tag_service]),
):
    domain_tags = service.get_all()
    return [TagRead.from_entity(tag) for tag in domain_tags]
