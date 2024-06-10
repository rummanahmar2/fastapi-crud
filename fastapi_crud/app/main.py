from pydantic import BaseModel
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException


class Item(BaseModel):
    name: str
    description: Optional[str] = None


db: Dict[int, Item] = {}
app = FastAPI()


# Create
@app.post("/items/")
async def create_item(item: Item):
    new_id = max(db.keys(), default=0) + 1
    db[new_id] = item
    return {"id": new_id, **item.dict()}


# Read
@app.get("/items/{item_id}/")
async def read_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]


@app.get("/items/")
async def read_items():
    if not db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db


# Update
@app.put("/items/{item_id}/")
async def update_item(item_id: int, item: Item):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    db[item_id] = item
    return {"id": item_id, **item.dict()}


# Delete
@app.delete("/items/{item_id}/")
async def delete_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]
    return {"message": "Item deleted successfully"}
