from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
import os

app = FastAPI()

# Allow frontend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["grocerydb"]
collection = db["items"]

# Pydantic models
class Item(BaseModel):
    name: str
    quantity: int

class ItemInDB(Item):
    id: str

def item_helper(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "quantity": item["quantity"],
    }

# Routes
@app.get("/api/items", response_model=list[ItemInDB])
async def get_items():
    items = await collection.find().to_list(100)
    return [item_helper(item) for item in items]

@app.post("/api/items", response_model=ItemInDB)
async def add_item(item: Item):
    result = await collection.insert_one(item.model_dump())
    new_item = await collection.find_one({"_id": result.inserted_id})
    return item_helper(new_item)

@app.put("/api/items/{item_id}", response_model=ItemInDB)
async def update_item(item_id: str, item: Item):
    result = await collection.update_one(
        {"_id": ObjectId(item_id)}, {"$set": item.dict()}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item = await collection.find_one({"_id": ObjectId(item_id)})
    return item_helper(updated_item)

@app.delete("/api/items/{item_id}")
async def delete_item(item_id: str):
    result = await collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}
