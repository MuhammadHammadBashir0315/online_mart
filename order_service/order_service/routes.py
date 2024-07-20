from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List 
from .models import Order, OrderItem, OrderStatus
from .database import get_session
from datetime import datetime

router = APIRouter()

@router.post("/orders/", response_model=Order)
def create_order(order: Order, session: Session = Depends(get_session)):
    for item in order.items:
        session.add(item)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

@router.get("/orders/", response_model=List[Order])
def read_orders(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    orders = session.exec(select(Order).offset(skip).limit(limit)).all()
    return orders

@router.get("/orders/{order_id}", response_model=Order)
def read_order(order_id: int, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/orders/{order_id}", response_model=Order)
def update_order(order_id: int, order: Order, session: Session = Depends(get_session)):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order_data = order.model_dump(exclude_unset=True)
    for key, value in order_data.items():
        setattr(db_order, key, value)
    
    db_order.updated_at = datetime.utcnow()
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@router.patch("/orders/{order_id}/status", response_model=Order)
def update_order_status(order_id: int, status: OrderStatus, session: Session = Depends(get_session)):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db_order.status = status
    db_order.updated_at = datetime.utcnow()
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

@router.get("/orders/{order_id}/items", response_model=List[OrderItem])
def read_order_items(order_id: int, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order.items