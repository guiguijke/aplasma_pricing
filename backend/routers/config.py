from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Config
from schemas import ConfigOut, ConfigUpdate

router = APIRouter(prefix="/api/config", tags=["config"])

DEFAULT_CONFIG = {
    "tax_rate": 0.22,
    "hourly_rates": {
        "welding_tig": 65.0,
        "welding_mig": 55.0,
        "laser": 70.0,
        "scanning": 80.0,
        "cad": 60.0,
    },
    "plasma_rates": {
        "cut_per_meter": 8.0,
        "pierce_cost": 0.30,
    },
    "post_process_rates": {
        "cleaning_per_m2": 8.0,
        "corten_per_m2": 25.0,
        "painting_standard_per_m2": 20.0,
        "painting_premium_per_m2": 35.0,
    },
    "complexity_range": {"min": 1.0, "max": 2.5},
    "laser_speed_factor": 200.0,
    "ref_price_per_kg": {
        "steel_mild": 0.90,
        "corten": 1.40,
        "stainless": 3.50,
        "aluminum": 2.80,
    },
}


def seed_config(db: Session):
    """Insert default config if not present."""
    for key, value in DEFAULT_CONFIG.items():
        if not db.query(Config).filter(Config.key == key).first():
            db.add(Config(key=key, value=value))
    db.commit()


def get_full_config(db: Session) -> dict:
    rows = db.query(Config).all()
    result = {**DEFAULT_CONFIG}
    for row in rows:
        result[row.key] = row.value
    return result


@router.get("", response_model=dict)
def read_config(db: Session = Depends(get_db)):
    return get_full_config(db)


@router.get("/{key}", response_model=ConfigOut)
def read_config_key(key: str, db: Session = Depends(get_db)):
    row = db.query(Config).filter(Config.key == key).first()
    if row is None:
        value = DEFAULT_CONFIG.get(key)
        return ConfigOut(key=key, value=value)
    return row


@router.put("/{key}", response_model=ConfigOut)
def update_config_key(key: str, body: ConfigUpdate, db: Session = Depends(get_db)):
    row = db.query(Config).filter(Config.key == key).first()
    if row is None:
        row = Config(key=key, value=body.value)
        db.add(row)
    else:
        row.value = body.value
    db.commit()
    db.refresh(row)
    return row
