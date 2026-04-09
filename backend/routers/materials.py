from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Material
from schemas import MaterialCreate, MaterialOut, MaterialUpdate

router = APIRouter(prefix="/api/materials", tags=["materials"])

SAMPLE_MATERIALS = [
    {"name": "Tôle S235 Brut 3mm 1000×2000", "material_type": "steel_mild", "product_type": "sheet",
     "finish": "brut", "thickness_mm": 3.0, "dimensions": {"width": 1000, "height": 2000}, "unit": "m2",
     "purchase_price": None, "supplier": None},
    {"name": "Tôle S235 DKP 3mm 1000×2000", "material_type": "steel_mild", "product_type": "sheet",
     "finish": "dkp", "thickness_mm": 3.0, "dimensions": {"width": 1000, "height": 2000}, "unit": "m2",
     "purchase_price": None, "supplier": None},
    {"name": "Tôle S235 Brut 5mm 1000×2000", "material_type": "steel_mild", "product_type": "sheet",
     "finish": "brut", "thickness_mm": 5.0, "dimensions": {"width": 1000, "height": 2000}, "unit": "m2",
     "purchase_price": None, "supplier": None},
    {"name": "Tôle S235 DKP 5mm 1000×2000", "material_type": "steel_mild", "product_type": "sheet",
     "finish": "dkp", "thickness_mm": 5.0, "dimensions": {"width": 1000, "height": 2000}, "unit": "m2",
     "purchase_price": None, "supplier": None},
    {"name": "Tôle Corten 3mm 1250×2500", "material_type": "corten", "product_type": "sheet",
     "finish": "brut", "thickness_mm": 3.0, "dimensions": {"width": 1250, "height": 2500}, "unit": "m2",
     "purchase_price": None, "supplier": None},
    {"name": "Tôle Inox 304 2mm 1000×2000", "material_type": "stainless", "product_type": "sheet",
     "finish": "brut", "thickness_mm": 2.0, "dimensions": {"width": 1000, "height": 2000}, "unit": "m2",
     "purchase_price": None, "supplier": None},
    {"name": "Tôle Alu 5083 3mm 1000×2000", "material_type": "aluminum", "product_type": "sheet",
     "finish": "brut", "thickness_mm": 3.0, "dimensions": {"width": 1000, "height": 2000}, "unit": "m2",
     "purchase_price": None, "supplier": None},
    {"name": "Tube S235 40×40×3", "material_type": "steel_mild", "product_type": "tube",
     "finish": "brut", "thickness_mm": 3.0, "dimensions": {"a": 40, "b": 40}, "unit": "ml",
     "purchase_price": None, "supplier": None},
    {"name": "Cornière S235 40×40×4", "material_type": "steel_mild", "product_type": "angle",
     "finish": "brut", "thickness_mm": 4.0, "dimensions": {"w": 40}, "unit": "ml",
     "purchase_price": None, "supplier": None},
    {"name": "Plat S235 30×5", "material_type": "steel_mild", "product_type": "flat_bar",
     "finish": "brut", "thickness_mm": 5.0, "dimensions": {"w": 30}, "unit": "ml",
     "purchase_price": None, "supplier": None},
]


def seed_materials(db: Session):
    if db.query(Material).count() == 0:
        for m in SAMPLE_MATERIALS:
            db.add(Material(**m))
        db.commit()


@router.get("", response_model=list[MaterialOut])
def list_materials(db: Session = Depends(get_db)):
    return db.query(Material).order_by(Material.material_type, Material.product_type, Material.name).all()


@router.post("", response_model=MaterialOut, status_code=201)
def create_material(body: MaterialCreate, db: Session = Depends(get_db)):
    mat = Material(**body.model_dump(), updated_at=datetime.utcnow())
    db.add(mat)
    db.commit()
    db.refresh(mat)
    return mat


@router.put("/{material_id}", response_model=MaterialOut)
def update_material(material_id: int, body: MaterialUpdate, db: Session = Depends(get_db)):
    mat = db.query(Material).filter(Material.id == material_id).first()
    if not mat:
        raise HTTPException(status_code=404, detail="Material not found")
    for field, value in body.model_dump().items():
        setattr(mat, field, value)
    mat.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(mat)
    return mat


@router.delete("/{material_id}", status_code=204)
def delete_material(material_id: int, db: Session = Depends(get_db)):
    mat = db.query(Material).filter(Material.id == material_id).first()
    if not mat:
        raise HTTPException(status_code=404, detail="Material not found")
    db.delete(mat)
    db.commit()
