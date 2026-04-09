"""
Post-processing calculator (cleaning, corten treatment, painting, custom).

Activity dict shape:
{
  "type": "post_process",
  "items": [
    {"subtype": "cleaning",  "area_m2": 1.2},
    {"subtype": "corten",    "area_m2": 1.2},
    {"subtype": "painting",  "area_m2": 1.2, "paint_type": "standard"},
    {"subtype": "custom",    "label": "Traitement thermique", "amount": 45.0},
  ]
}
"""


def calculate(params: dict, config: dict) -> list[dict]:
    post_rates = config.get("post_process_rates", {})
    cleaning_rate    = post_rates.get("cleaning_per_m2", 8.0)      # €/m²
    corten_rate      = post_rates.get("corten_per_m2", 25.0)        # €/m²  (acid + aging)
    painting_std     = post_rates.get("painting_standard_per_m2", 20.0)
    painting_premium = post_rates.get("painting_premium_per_m2", 35.0)

    lines = []

    for item in params.get("items", []):
        subtype = item.get("subtype", "custom")

        if subtype == "cleaning":
            area = float(item.get("area_m2", 0))
            lines.append({
                "label": f"Nettoyage tôle ({area} m²)",
                "amount": round(area * cleaning_rate, 2),
                "is_estimated": False,
            })

        elif subtype == "corten":
            area = float(item.get("area_m2", 0))
            lines.append({
                "label": f"Décapage + vieillissement Corten ({area} m²)",
                "amount": round(area * corten_rate, 2),
                "is_estimated": False,
            })

        elif subtype == "painting":
            area = float(item.get("area_m2", 0))
            paint_type = item.get("paint_type", "standard")
            rate = painting_premium if paint_type == "premium" else painting_std
            lines.append({
                "label": f"Peinture {paint_type} ({area} m²)",
                "amount": round(area * rate, 2),
                "is_estimated": False,
            })

        elif subtype == "custom":
            label = item.get("label", "Post-traitement")
            amount = float(item.get("amount", 0))
            lines.append({
                "label": label,
                "amount": round(amount, 2),
                "is_estimated": False,
            })

    return lines
