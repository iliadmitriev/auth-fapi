from typing import Optional, List
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI()


@app.post(
    "/items/",
    name="Create new Item",
    description="Creates new item instance with post query",
    response_model=Item,
    tags=['items']
)
async def create_item(item: Item) -> Item:
    return item


@app.get(
    "/items/",
    name="Get items list",
    description="Retrieve items list from, with query",
    response_model=List[Item],
    tags=['items']
)
async def create_item(q: Optional[str] = None) -> List[Item]:
    item = Item(name="Orange Juice", price=9.90)
    return [item]


@app.get("/")
async def root():
    return {"message": "Hello World"}
