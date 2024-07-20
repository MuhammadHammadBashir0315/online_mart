from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from .models import InventoryItem, InventoryUpdate
from .database import get_session
from datetime import datetime

router = APIRouter()

@router.post("/inventory/", response_model=InventoryItem)
def create_inventory_item(item: InventoryItem, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@router.get("/inventory/", response_model=List[InventoryItem])
def read_inventory(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    items = session.exec(select(InventoryItem).offset(skip).limit(limit)).all()
    return items

@router.get("/inventory/{product_id}", response_model=InventoryItem)
def read_inventory_item(product_id: int, session: Session = Depends(get_session)):
    item = session.exec(select(InventoryItem).where(InventoryItem.product_id == product_id)).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return item

@router.put("/inventory/{product_id}", response_model=InventoryItem)
def update_inventory_item(product_id: int, item: InventoryItem, session: Session = Depends(get_session)):
    db_item = session.exec(select(InventoryItem).where(InventoryItem.product_id == product_id)).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    item_data = item.dict(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    
    db_item.last_updated = datetime.utcnow()
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@router.post("/inventory/update", response_model=InventoryItem)
def update_inventory(update: InventoryUpdate, session: Session = Depends(get_session)):
    db_item = session.exec(select(InventoryItem).where(InventoryItem.product_id == update.product_id)).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    db_item.quantity += update.quantity_change
    db_item.last_updated = datetime.utcnow()
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@router.get("/inventory/low-stock", response_model=List[InventoryItem])
def get_low_stock_items(threshold: int = 10, session: Session = Depends(get_session)):
    items = session.exec(select(InventoryItem).where(InventoryItem.quantity < threshold)).all()
    return items