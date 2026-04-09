"""
Estimates material price from weight when purchase_price is unknown.
Densities in kg/dm³, reference market prices in €/kg (configurable via Settings).
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


def estimate_price(
    material_type: str,
    product_type: str,
    dimensions: dict | None,
    thickness_mm: float | None,
    quantity: float,
    ref_price_per_kg: dict[str, float] | None = None,
) -> float:
    """Returns estimated price in € for the given quantity."""
    refs = ref_price_per_kg or DEFAULT_REF_PRICE_PER_KG
    density = DENSITY.get(material_type, 7.85)
    ref = refs.get(material_type, 1.0)
    volume = _volume_dm3(product_type, dimensions or {}, thickness_mm, quantity)
    weight_kg = volume * density
    return round(weight_kg * ref, 2)
