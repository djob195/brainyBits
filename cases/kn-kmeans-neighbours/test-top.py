import json
import math
import random
from pathlib import Path
from shapely.geometry import shape, Point
from utils.geo import haversine_distance, bearing
import heapq
import time

BEARING_STEP = 5

BASE_DIR = Path(__file__).resolve().parent
zone_json_path = BASE_DIR / "database" / "zones-geo.json"
bearing_dir = BASE_DIR / "database" / "bearing_groups"
warehouses_path = BASE_DIR / "database" / "warehouses-geo.json"
customers_path = BASE_DIR / "database" / "customer_mockup.json"

with zone_json_path.open(encoding="utf-8") as f:
    zones_geojson = json.load(f)

with warehouses_path.open(encoding="utf-8") as f:
    warehouses_geojson = json.load(f)

with customers_path.open(encoding="utf-8") as f:
    data_customer = json.load(f)

zone_feature = random.choice(zones_geojson["features"])
zone_id_ref = zone_feature["properties"]["zone"]
geom = shape(zone_feature["geometry"])

if geom.geom_type == "MultiPolygon":
    geom = max(geom.geoms, key=lambda g: g.area)

def random_point_in_polygon(polygon):
    minx, miny, maxx, maxy = polygon.bounds
    while True:
        p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if polygon.contains(p):
            return p

point = random_point_in_polygon(geom)

def get_warehouse_point_by_zone(zone_id):
    for feature in warehouses_geojson["features"]:
        if feature["properties"].get("zone") == zone_id:
            coords = feature["geometry"]["coordinates"]
            return Point(coords[0], coords[1])
    return None

warehouse_ref = get_warehouse_point_by_zone(zone_id_ref)
warehouse = {"lat": warehouse_ref.y, "lon": warehouse_ref.x}

start = time.perf_counter()

dist_m = haversine_distance(
    warehouse["lat"], warehouse["lon"],
    point.y, point.x,
    unit="meters"
)

bear = bearing(
    warehouse["lat"], warehouse["lon"],
    point.y, point.x
)

bear_ref = math.ceil(bear / BEARING_STEP) * BEARING_STEP
bearing_file = bearing_dir / f"{bear_ref}.json"

with bearing_file.open(encoding="utf-8") as f:
    data_clustering = json.load(f) 

client_distances = []
for _, client_idx in data_clustering:
    client = data_customer[client_idx]
    tmp = client["coordinates"]
    dist_to_point = haversine_distance(
        tmp[1], tmp[0],
        point.y, point.x,
        unit="meters"
    )
    heapq.heappush(client_distances,(dist_to_point, client_idx))


print(f"random point: {point.y}, {point.x}")

for _ in range(3):
    if not client_distances:
        continue
    (dist,client_idx) = heapq.heappop(client_distances)
    client = data_customer[client_idx]
    wh = client["warehouse"]
    full_name = client["full_name"]
    print(f"client {full_name}: Point({wh['lat']}, {wh['lon']}), Distance={dist:.2f} m")

end = time.perf_counter()

print(f"Get top 3 on {end - start:.6f} seconds")