"""
Estimates material price from weight when purchase_price is unknown.
Densities in kg/dm³, reference market prices in €/kg (configurable via Settings).

When materials with known prices exist in the database, computes an average €/kg
per material_type to improve estimation accuracy.
"""

# kg/dm³
DENSITY: dict[str, float] = {
    "steel_mild": 7.85,
    "corten":     7.85,
    "stainless":  7.93,
    "aluminum":   2.70,
}

# Default market reference prices €/kg — overridden by config "ref_price_per_kg"
DEFAULT_REF_PRICE_PER_KG: dict[str, float] = {
    "steel_mild": 0.90,
    "corten":     1.40,
    "stainless":  3.50,
    "aluminum":   2.80,
}


def _volume_dm3(product_type: str, dimensions: dict, thickness_mm: float | None, quantity: float) -> float:
    """
    Returns volume in dm³ for a given quantity (m² for sheets, ml for profiles).
    quantity: m² (sheets) or meters (profiles)
    """
    t = (thickness_mm or 3.0) / 10.0  # mm → dm

    if product_type == "sheet":
        # quantity in m² → dm²
        area_dm2 = quantity * 100.0
        return area_dm2 * t

    # Profiles: quantity in meters → dm
    length_dm = quantity * 10.0
    dims = dimensions or {}

    if product_type == "tube":
        a = dims.get("a", 40) / 10.0   # dm
        b = dims.get("b", 40) / 10.0
        wall = t
        # hollow square/rect cross-section area
        outer = a * b
        inner = (a - 2 * wall) * (b - 2 * wall)
        return max(outer - inner, 0) * length_dm

    if product_type == "round_bar":
        import math
        d = dims.get("d", 20) / 10.0 / 2.0   # radius in dm
        return math.pi * d ** 2 * length_dm

    if product_type in ("flat_bar", "angle", "channel"):
        # approximate: width × thickness cross-section
        w = dims.get("w", 30) / 10.0
        return w * t * length_dm

    # fallback: treat as solid bar 30mm × thickness
    return 0.03 * t * length_dm


def weight_per_unit(product_type: str, dimensions: dict | None, thickness_mm: float | None, material_type: str) -> float:
    """Returns weight in kg for 1 unit (1 m² for sheets, 1 ml for profiles, 1 for kg)."""
    density = DENSITY.get(material_type, 7.85)
    volume = _volume_dm3(product_type, dimensions or {}, thickness_mm, 1.0)
    return volume * density


def item_weight_kg(product_type: str, dimensions: dict | None, thickness_mm: float | None, material_type: str, unit: str) -> float:
    """
    Returns the total weight in kg for the item as purchased.
    - Sheets: weight of the full sheet (dimensions width×height)
    - Profiles (ml): weight per meter
    - kg: 1 kg
    """
    if unit == "kg":
        return 1.0
    density = DENSITY.get(material_type, 7.85)
    if product_type == "sheet" and dimensions:
        # Full sheet area in m²
        w_mm = dimensions.get("width", 1000)
        h_mm = dimensions.get("height", 2000)
        full_area_m2 = (w_mm * h_mm) / 1_000_000
        volume = _volume_dm3("sheet", dimensions, thickness_mm, full_area_m2)
        return volume * density
    # Profiles: per meter
    volume = _volume_dm3(product_type, dimensions or {}, thickness_mm, 1.0)
    return volume * density


def price_per_kg(purchase_price: float, product_type: str, dimensions: dict | None,
                 thickness_mm: float | None, material_type: str, unit: str) -> float | None:
    """Returns €/kg for a material with known purchase_price, or None."""
    if purchase_price is None or purchase_price <= 0:
        return None
    w = item_weight_kg(product_type, dimensions, thickness_mm, material_type, unit)
    if w <= 0:
        return None
    return round(purchase_price / w, 2)


def compute_avg_price_per_kg(materials: list[dict]) -> dict[str, dict]:
    """
    From a list of material dicts (with purchase_price, unit, etc.),
    compute the average €/kg per material_type.

    purchase_price semantics:
    - Sheets (unit m²): price of the full sheet (not per m²)
    - Profiles (unit ml): price per meter
    - kg: price per kg

    Returns {material_type: {"avg": float, "count": int, "min": float, "max": float}}
    """
    from collections import defaultdict
    buckets: dict[str, list[float]] = defaultdict(list)

    for mat in materials:
        ppkg = price_per_kg(
            mat.get("purchase_price"),
            mat.get("product_type", "sheet"),
            mat.get("dimensions"),
            mat.get("thickness_mm"),
            mat.get("material_type", "steel_mild"),
            mat.get("unit", "m2"),
        )
        if ppkg is not None:
            buckets[mat.get("material_type", "steel_mild")].append(ppkg)

    result = {}
    for mat_type, prices in buckets.items():
        if prices:
            avg = round(sum(prices) / len(prices), 2)
            result[mat_type] = {
                "avg": avg,
                "count": len(prices),
                "min": round(min(prices), 2),
                "max": round(max(prices), 2),
            }
    return result


def estimate_price(
    material_type: str,
    product_type: str,
    dimensions: dict | None,
    thickness_mm: float | None,
    quantity: float,
    ref_price_per_kg: dict[str, float] | None = None,
    avg_price_per_kg: dict[str, dict] | None = None,
) -> float:
    """
    Returns estimated price in € for the given quantity.
    Priority: avg from DB materials > config ref > hardcoded default.
    """
    # Pick best available reference price
    if avg_price_per_kg and material_type in avg_price_per_kg:
        ref = avg_price_per_kg[material_type]["avg"]
    elif ref_price_per_kg and material_type in ref_price_per_kg:
        ref = ref_price_per_kg[material_type]
    else:
        ref = DEFAULT_REF_PRICE_PER_KG.get(material_type, 1.0)

    density = DENSITY.get(material_type, 7.85)
    volume = _volume_dm3(product_type, dimensions or {}, thickness_mm, quantity)
    weight_kg = volume * density
    return round(weight_kg * ref, 2)
