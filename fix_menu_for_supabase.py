import json
import csv
import uuid

SUPABASE_BUCKET_URL = "https://nezbktuqqqprshhaenix.supabase.co/storage/v1/object/public/menu-images/"

with open("backend/menu.json", "r", encoding="utf-8") as f:
    menu = json.load(f)

fixed_menu = []
for item in menu:
    # Get filename from old image URL
    filename = item.get("image", "").split("/")[-1]
    # Build new Supabase image URL
    item["image"] = SUPABASE_BUCKET_URL + filename if filename else ""

    # Always generate a new valid UUID for id
    item["id"] = str(uuid.uuid4())

    # name, category: required, must not be empty
    item["name"] = item.get("name") or "Unnamed"
    item["category"] = item.get("category") or "Uncategorized"

    # extras, pizzaSubcategory: optional text, use empty string if missing
    item["extras"] = item.get("extras") or ""
    item["pizzaSubcategory"] = item.get("pizzaSubcategory") or ""

    # price: must be a number, default to 0.0 if missing/invalid
    try:
        item["price"] = float(item.get("price", 0))
    except Exception:
        item["price"] = 0.0

    # sizes, extraOptions: must be valid JSON (use [] if missing)
    item["sizes"] = item.get("sizes") if isinstance(item.get("sizes"), list) else []
    item["extraOptions"] = item.get("extraOptions") if isinstance(item.get("extraOptions"), list) else []

    fixed_menu.append(item)

# Save as new JSON (for reference)
with open("backend/menu_supabase.json", "w", encoding="utf-8") as f:
    json.dump(fixed_menu, f, ensure_ascii=False, indent=2)

# Save as CSV for Supabase import (JSON columns as raw JSON)
with open("backend/menu_supabase.csv", "w", encoding="utf-8", newline="") as f:
    fieldnames = [
        "id", "name", "category", "extras", "price", "sizes", "image", "extraOptions", "pizzaSubcategory"
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in fixed_menu:
        csv_row = row.copy()
        csv_row["sizes"] = json.dumps(csv_row["sizes"], ensure_ascii=False)
        csv_row["extraOptions"] = json.dumps(csv_row["extraOptions"], ensure_ascii=False)
        # Ensure all fieldnames are present in the row
        for key in fieldnames:
            if key not in csv_row:
                csv_row[key] = ""
        writer.writerow(csv_row)