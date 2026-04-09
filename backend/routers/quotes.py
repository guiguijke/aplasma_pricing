from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Quote, Material
from schemas import QuoteCreate, QuoteUpdate, QuoteOut, QuoteListItem, CalculateRequest, CalculateResponse
from routers.config import get_full_config
from calculators import plasma, welding, laser, scanning, post_process
from calculators.material_estimator import compute_avg_price_per_kg

router = APIRouter(prefix="/api", tags=["quotes"])

CALCULATORS = {
    "plasma":       plasma.calculate,
    "welding":      welding.calculate,
    "laser":        laser.calculate,
    "scanning":     scanning.calculate,
    "cad":          scanning.calculate,
    "post_process": post_process.calculate,
}


def run_calculation(activities: list[dict], config: dict) -> dict:
    all_lines = []
    for activity in activities:
        atype = activity.get("type")
        calc = CALCULATORS.get(atype)
        if calc:
            lines = calc(activity, config)
            all_lines.extend(lines)

    has_estimates = any(line.get("is_estimated", False) for line in all_lines)
    total_ht = round(sum(line["amount"] for line in all_lines), 2)
    material_cost_ht = round(sum(line["amount"] for line in all_lines if line.get("is_material")), 2)
    tax_rate = config.get("tax_rate", 0.22)
    # Net = (total HT − coût matière) × (1 − charges) : on ne gagne rien sur la matière
    net_estimated = round((total_ht - material_cost_ht) * (1 - tax_rate), 2)

    return {
        "lines": all_lines,
        "total_ht": total_ht,
        "material_cost_ht": material_cost_ht,
        "net_estimated": net_estimated,
        "has_estimates": has_estimates,
        "tax_rate": tax_rate,
    }


@router.post("/calculate", response_model=CalculateResponse)
def calculate(body: CalculateRequest, db: Session = Depends(get_db)):
    config = get_full_config(db)
    if body.tax_rate is not None:
        config["tax_rate"] = body.tax_rate
    # Compute dynamic avg €/kg from materials with known prices
    rows = db.query(Material).filter(Material.purchase_price.isnot(None)).all()
    mat_dicts = [
        {"purchase_price": m.purchase_price, "unit": m.unit, "material_type": m.material_type,
         "product_type": m.product_type, "dimensions": m.dimensions, "thickness_mm": m.thickness_mm}
        for m in rows
    ]
    config["avg_price_per_kg"] = compute_avg_price_per_kg(mat_dicts)
    return run_calculation(body.activities, config)


@router.get("/quotes", response_model=list[QuoteListItem])
def list_quotes(db: Session = Depends(get_db)):
    return db.query(Quote).order_by(Quote.created_at.desc()).all()


@router.post("/quotes", response_model=QuoteOut, status_code=201)
def create_quote(body: QuoteCreate, db: Session = Depends(get_db)):
    quote = Quote(
        reference=body.reference,
        activities=body.activities,
        total_ht=body.total_ht,
        net_estimated=body.net_estimated,
        has_estimates=1 if body.has_estimates else 0,
        notes=body.notes,
        lines=body.lines,
    )
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return quote


@router.put("/quotes/{quote_id}", response_model=QuoteOut)
def update_quote(quote_id: int, body: QuoteUpdate, db: Session = Depends(get_db)):
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    quote.reference = body.reference
    quote.activities = body.activities
    quote.total_ht = body.total_ht
    quote.net_estimated = body.net_estimated
    quote.has_estimates = 1 if body.has_estimates else 0
    quote.notes = body.notes
    quote.lines = body.lines
    db.commit()
    db.refresh(quote)
    return quote


@router.get("/quotes/{quote_id}", response_model=QuoteOut)
def get_quote(quote_id: int, db: Session = Depends(get_db)):
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote


@router.delete("/quotes/{quote_id}", status_code=204)
def delete_quote(quote_id: int, db: Session = Depends(get_db)):
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    db.delete(quote)
    db.commit()
