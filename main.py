import uvicorn
from typing import Optional, List
from fastapi import FastAPI, status
from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = Field(..., title="Item name", example="Banana")
    description: Optional[str] = Field(None, title="Item description", example="One pound of banana")
    price: float = Field(..., title="Price of item without tax", example=4.99)
    tax: Optional[float] = Field(None, title="Tax amount", example="null")


app = FastAPI()


@app.post(
    "/items/",
    status_code=status.HTTP_201_CREATED,
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


if __name__ == "__main__":  # pragma: no cover
    uvicorn.run(app, host="0.0.0.0", port=8000)
