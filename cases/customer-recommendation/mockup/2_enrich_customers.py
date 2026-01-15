import json
import os
from shapely.geometry import shape
from utils.geo import  bearing
import time

start = time.time()

base_path = os.path.dirname(os.path.dirname(__file__))


warehouses_path = os.path.join(base_path, "database", "warehouses-geo.json")
customers_path = os.path.join(base_path, "database", "customer_mockup.json")


with open(warehouses_path, "r", encoding="utf-8") as f:
    warehouses_geo = json.load(f)


with open(customers_path, "r", encoding="utf-8") as f:
    customers = json.load(f)


warehouse_by_zone = {}

for feature in warehouses_geo["features"]:
    zone = feature["properties"].get("zone") or feature["properties"].get("zona")
    geom = shape(feature["geometry"])
    centroid = geom.centroid

    warehouse_by_zone[zone] = {
        "lat": centroid.y,
        "lon": centroid.x
    }

enriched_customers = []

for customer in customers:
    zone = customer["zone"]

    if zone not in warehouse_by_zone:
        continue

    wh = warehouse_by_zone[zone]

    customer_lat = customer["coordinates"][1]
    customer_lon = customer["coordinates"][0]

    bear = bearing(
        wh["lat"], wh["lon"],
        customer_lat, customer_lon
    )

    enriched_customer = {
        **customer,
        "warehouse": {
            "lat": wh["lat"],
            "lon": wh["lon"]
        },
        "bearing_degrees": round(bear, 2)
    }

    enriched_customers.append(enriched_customer)

with open(customers_path, "w", encoding="utf-8") as f:
    json.dump(enriched_customers, f, indent=2, ensure_ascii=False)

end = time.time()

print(f"{len(enriched_customers)} customers enriched and saved to: {customers_path},  time: {end - start:.6f} seconds")