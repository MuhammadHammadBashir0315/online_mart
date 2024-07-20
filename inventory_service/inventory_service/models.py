from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class InventoryItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(index=True)
    quantity: int
    last_updated: datetime = Field(default_factory=datetime.now(datetime.UTC))

class InventoryUpdate(SQLModel):
    product_id: int
    quantity_change: int