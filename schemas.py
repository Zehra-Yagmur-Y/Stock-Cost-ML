from pydantic import BaseModel
from datetime import datetime


# Stok ekleme/güncelleme için kullanılacak şema
class MainStockBase(BaseModel):
    material_name: str
    material_code: str
    total_quantity: int


# Stok oluşturma şeması
class MainStockCreate(MainStockBase):
    pass


# Stok okuma (GET) şeması
class MainStockRead(MainStockBase):
    id: int
    last_updated: datetime

    class Config:
        orm_mode = True
