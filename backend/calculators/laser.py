"""
Laser engraving calculator (MOPA 60W).

Activity dict shape:
{
  "type": "laser",
  "engraved_area_cm2": 50.0,
  "density": 0.6,          # slider 0.1–1.0 (fill density of the pattern)
  "piece_count": 4,
}

laser_speed_factor (cm²/h) is configurable in Settings.
"""


def calculate(params: dict, config: dict) -> list[dict]:
    hourly_rates = config.get("hourly_rates", {})
    rate = hourly_rates.get("laser", 70.0)
    laser_speed_factor = config.get("laser_speed_factor", 200.0)  # cm²/h at density 1.0

    area = float(params.get("engraved_area_cm2", 0))
    density = float(params.get("density", 0.5))
    pieces = int(params.get("piece_count", 1))

    if area <= 0 or pieces <= 0:
        return []

    # Effective time: area × density × pieces / speed
    time_hours = (area * density * pieces) / laser_speed_factor
    amount = time_hours * rate

    return [{
        "label": f"Gravure laser MOPA ({area} cm² × densité {density:.1f} × {pieces} pcs)",
        "amount": round(amount, 2),
        "is_estimated": False,
    }]
