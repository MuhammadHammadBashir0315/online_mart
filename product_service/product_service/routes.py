from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from .models import Product
from .database import get_session

router = APIRouter()

@router.post("/products/", response_model=Product)
def create_product(product: Product, session:Session = Depends(get_session)):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router.get("/products/" , response_model=List[Product])
def read_products(skip: int=0, limit:int = 100, session: Session=Depends(get_session)):
    products = session.exec(select(Product).offset(skip).limit(limit)).all()
    return products

@router.post("products/{product_id}", response_model=Product)
def read_product(product_id , session:Session=Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{product_id}" , response_model=Product)
def update_product(product_id : int, product: Product,  session : Session = Depends(get_session)):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404 , detail="not found")
    product_data = product.model_dump(exclude_unset=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)
    
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@router.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    session.delete(product)
    session.commit()
    return product
