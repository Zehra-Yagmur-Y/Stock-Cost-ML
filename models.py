from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from isg_api.database import Base  # Doğru import

class MainStock(Base):  # `Base`'den miras almalı
    __tablename__ = "main_stock"
    __table_args__ = {"extend_existing": True}  #  Hata çözümü

    id = Column(Integer, primary_key=True, index=True)
    material_name = Column(String(100), nullable=False)
    material_code = Column(String(50), unique=True, nullable=False)
    total_quantity = Column(Integer, default=0)
    last_updated = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    department = Column(String)  