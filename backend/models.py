from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, JSON
from database import Base


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    activities = Column(JSON, nullable=False)  # list of activity dicts with params + subtotals
    total_ht = Column(Float, nullable=False)
    net_estimated = Column(Float, nullable=False)
    has_estimates = Column(Integer, default=0)  # 1 if any line uses estimated material price
    notes = Column(Text, default="")
    lines = Column(JSON, nullable=True)  # list of {label, amount, is_estimated} — saved at quote time


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    material_type = Column(String, nullable=False)  # steel_mild | corten | stainless | aluminum
    product_type = Column(String, nullable=False)   # sheet | tube | flat_bar | angle | channel | round_bar | other
    thickness_mm = Column(Float, nullable=True)
    dimensions = Column(JSON, nullable=True)        # {"width": 1000, "height": 2000} or {"a": 40, "b": 40}
    unit = Column(String, nullable=False)           # m2 | kg | ml
    purchase_price = Column(Float, nullable=True)   # null = unknown → use estimated price
    supplier = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Config(Base):
    __tablename__ = "config"

    key = Column(String, primary_key=True)
    value = Column(JSON, nullable=False)
