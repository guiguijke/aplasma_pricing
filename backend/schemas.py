from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel


# ── Material ──────────────────────────────────────────────────────────────────

class MaterialBase(BaseModel):
    name: str
    material_type: str       # steel_mild | corten | stainless | aluminum
    product_type: str        # sheet | tube | flat_bar | angle | channel | round_bar | other
    finish: str = "brut"     # brut | dkp | galva | larme
    thickness_mm: Optional[float] = None
    dimensions: Optional[dict] = None
    unit: str                # m2 | kg | ml
    purchase_price: Optional[float] = None
    supplier: Optional[str] = None
    suffix: Optional[str] = None
    notes: Optional[str] = None


class MaterialCreate(MaterialBase):
    pass


class MaterialUpdate(MaterialBase):
    pass


class MaterialOut(MaterialBase):
    id: int
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Config ────────────────────────────────────────────────────────────────────

class ConfigOut(BaseModel):
    key: str
    value: Any

    model_config = {"from_attributes": True}


class ConfigUpdate(BaseModel):
    value: Any


# ── Quote ─────────────────────────────────────────────────────────────────────

class QuoteCreate(BaseModel):
    reference: str
    activities: list[dict]
    total_ht: float
    net_estimated: float
    has_estimates: bool = False
    notes: str = ""
    lines: Optional[list[dict]] = None


class QuoteUpdate(BaseModel):
    reference: str
    activities: list[dict]
    total_ht: float
    net_estimated: float
    has_estimates: bool = False
    notes: str = ""
    lines: Optional[list[dict]] = None


class QuoteOut(BaseModel):
    id: int
    reference: str
    created_at: datetime
    activities: list[dict]
    total_ht: float
    net_estimated: float
    has_estimates: bool
    notes: str
    lines: Optional[list[dict]] = None

    model_config = {"from_attributes": True}


class QuoteListItem(BaseModel):
    id: int
    reference: str
    created_at: datetime
    total_ht: float
    net_estimated: float
    has_estimates: bool

    model_config = {"from_attributes": True}


# ── Calculate request ─────────────────────────────────────────────────────────

class CalculateRequest(BaseModel):
    activities: list[dict]   # each dict has "type" + activity-specific params
    tax_rate: Optional[float] = None  # override config if provided


class CalculateResponse(BaseModel):
    lines: list[dict]        # each line: label, amount, is_estimated, is_material?
    total_ht: float
    material_cost_ht: float  # sum of material lines (excluded from net)
    net_estimated: float
    has_estimates: bool
    tax_rate: float
