"""
Welding calculator (TIG / MIG-MAG).

Activity dict shape:
{
  "type": "welding",
  "weld_type": "tig",     # "tig" | "mig_mag"
  "hours": 2.5,
  "complexity": 1.4,      # slider 1.0–2.5
}
"""


def calculate(params: dict, config: dict) -> list[dict]:
    hourly_rates = config.get("hourly_rates", {})

    weld_type = params.get("weld_type", "tig")
    hours = float(params.get("hours", 0))
    complexity = float(params.get("complexity", 1.0))

    rate_key = "welding_tig" if weld_type == "tig" else "welding_mig"
    rate = hourly_rates.get(rate_key, 65.0)

    amount = hours * rate * complexity
    label_type = "TIG" if weld_type == "tig" else "MIG/MAG"

    return [{
        "label": f"Soudure {label_type} ({hours}h × ×{complexity:.1f})",
        "amount": round(amount, 2),
        "is_estimated": False,
    }]
