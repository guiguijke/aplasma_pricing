"""
3D scanning and CAD plans calculator.

Activity dict shape:
{
  "type": "scanning",       # or "cad"
  "activity_subtype": "scanning",   # "scanning" | "cad"
  "hours": 3.0,
  "complexity": 1.2,        # slider 1.0–2.5
}
"""


def calculate(params: dict, config: dict) -> list[dict]:
    hourly_rates = config.get("hourly_rates", {})

    subtype = params.get("activity_subtype", params.get("type", "scanning"))
    hours = float(params.get("hours", 0))
    complexity = float(params.get("complexity", 1.0))

    if subtype == "cad":
        rate = hourly_rates.get("cad", 60.0)
        label = f"Plans CAO ({hours}h × ×{complexity:.1f})"
    else:
        rate = hourly_rates.get("scanning", 80.0)
        label = f"Scan 3D ({hours}h × ×{complexity:.1f})"

    amount = hours * rate * complexity

    return [{
        "label": label,
        "amount": round(amount, 2),
        "is_estimated": False,
    }]
