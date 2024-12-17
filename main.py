from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Item
import crud

# Initialize FastAPI app
app = FastAPI()

# Create item endpoint
@app.post("/items/", response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db: Session = Depends(database.get_db)):
    return crud.create_item(db=db, item=item)

# Read item by ID endpoint
@app.get("/items/{item_id}", response_model=schemas.Item)
async def read_item(item_id: int, db: Session = Depends(database.get_db)):
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Get all items endpoint with pagination
@app.get("/items/", response_model=list[schemas.Item])
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    items = crud.get_items(db=db, skip=skip, limit=limit)
    return items
