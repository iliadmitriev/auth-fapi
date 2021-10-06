from typing import List

from fastapi import APIRouter
from starlette import status

from schemas.items import Item

router = APIRouter()


@router.post(
    "/items/",
    status_code=status.HTTP_201_CREATED,
    name="Create new Item",
    description="Creates new item instance with post query",
    response_model=Item
)
async def create_item(item: Item) -> Item:
    return item


@router.get(
    "/items/",
    name="Get items list",
    description="Retrieve items list from, with query",
    response_model=List[Item]
)
async def get_items() -> List[Item]:
    item = Item(name="Orange Juice", price=9.90)
    return [item]