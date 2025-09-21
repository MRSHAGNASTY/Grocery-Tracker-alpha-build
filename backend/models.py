from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String)
    prices = relationship("PriceEntry", back_populates="store")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    unit = Column(String)
    prices = relationship("PriceEntry", back_populates="product")

class PriceEntry(Base):
    __tablename__ = "price_entries"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    price = Column(Float, nullable=False)
    date_recorded = Column(DateTime, default=datetime.utcnow)
    quantity = Column(Float, default=1.0)

    product = relationship("Product", back_populates="prices")
    store = relationship("Store", back_populates="prices")

