"""
Plasma cutting calculator.

Activity dict shape:
{
  "type": "plasma",
  "cut_length_mm": 12000,
  "pierce_count": 24,
  "material_id": 3,          # optional — resolved to material data by the router
  "material_name": "Acier S235 3mm",
  "material_type": "steel_mild",
  "product_type": "sheet",
  "thickness_mm": 3.0,
  "dimensions": {"width": 1000, "height": 2000},
  "sheet_area_m2": 0.5,
  "sheet_billing": "partial",   # "full" | "partial"
  "purchase_price": 12.50,      # null → estimated
  "ref_price_per_kg": {...},    # from config, used when purchase_price is null
}
"""

from calculators.material_estimator import estimate_price


def calculate(params: dict, config: dict) -> list[dict]:
    """
    Returns a list of price lines:
    [{"label": str, "amount": float, "is_estimated": bool}, ...]
    """
    plasma_rates = config.get("plasma_rates", {})
    cut_per_meter = plasma_rates.get("cut_per_meter", 8.0)
    pierce_cost_unit = plasma_rates.get("pierce_cost", 0.30)

    lines = []

    # ── Material cost ────────────────────────────────────────────────────────
    sheet_area = params.get("sheet_area_m2", 0.0)
    purchase_price = params.get("purchase_price")
    material_margin = config.get("material_margin", 0.0)
    is_estimated = False

    if sheet_area > 0:
        if purchase_price is not None:
            price_per_unit = float(purchase_price)
        else:
            # Estimate from weight — use avg from DB materials if available
            price_per_unit = estimate_price(
                material_type=params.get("material_type", "steel_mild"),
                product_type=params.get("product_type", "sheet"),
                dimensions=params.get("dimensions"),
                thickness_mm=params.get("thickness_mm"),
                quantity=sheet_area,
                ref_price_per_kg=params.get("ref_price_per_kg"),
                avg_price_per_kg=config.get("avg_price_per_kg"),
            )
            is_estimated = True

        billing = params.get("sheet_billing", "partial")
        if billing == "full":
            # Price for the full standard sheet, prorate to billed area
            full_dims = params.get("dimensions", {"width": 1000, "height": 2000})
            full_area = (full_dims.get("width", 1000) * full_dims.get("height", 2000)) / 1_000_000
            material_cost = price_per_unit * full_area if full_area > 0 else price_per_unit * sheet_area
        else:
            material_cost = price_per_unit * sheet_area

        # Apply material margin
        material_cost_with_margin = material_cost * (1 + material_margin)

        margin_label = f" +{round(material_margin * 100)}% marge" if material_margin > 0 else ""
        lines.append({
            "label": f"Matière — {params.get('material_name', 'tôle')} ({sheet_area} m²){margin_label}",
            "amount": round(material_cost_with_margin, 2),
            "is_estimated": is_estimated,
            "is_material": True,
        })

    # ── Cutting cost ─────────────────────────────────────────────────────────
    cut_length_mm = params.get("cut_length_mm", 0)
    if cut_length_mm > 0:
        cut_meters = cut_length_mm / 1000.0
        cut_cost = cut_meters * cut_per_meter
        lines.append({
            "label": f"Découpe plasma ({cut_meters:.2f} m)",
            "amount": round(cut_cost, 2),
            "is_estimated": False,
        })

    # ── Piercing cost ────────────────────────────────────────────────────────
    pierce_count = params.get("pierce_count", 0)
    if pierce_count > 0:
        pierce_cost = pierce_count * pierce_cost_unit
        lines.append({
            "label": f"Perçages (×{pierce_count})",
            "amount": round(pierce_cost, 2),
            "is_estimated": False,
        })

    return lines
