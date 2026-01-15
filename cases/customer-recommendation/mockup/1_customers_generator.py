import json
import random
from shapely.geometry import shape, Point
import os
import uuid
from faker import Faker
import time

start = time.perf_counter()

# Configuración
points_per_zone = 200
generated_points = []
existing_coords = set()  
precision = 6  

base_path = os.path.dirname(os.path.dirname(__file__))
geojson_path = os.path.join(base_path, "database", "zones-geo.json")
output_path = os.path.join(base_path, "database", "customer_mockup.json")

with open(geojson_path, "r", encoding="utf-8") as f:
    data = json.load(f)

fake = Faker('es_ES')

def random_point_in_polygon(polygon):
    minx, miny, maxx, maxy = polygon.bounds
    while True:
        p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if polygon.contains(p):
            return p

for feature in data["features"]:
    geom = shape(feature["geometry"])
    zone_id = feature["properties"].get("zone") or feature["properties"].get("zona")
    
    while len([p for p in generated_points if p["zone"] == zone_id]) < points_per_zone:
        uid = str(uuid.uuid4())
        p = random_point_in_polygon(geom)
        
        coords_tuple = (round(p.x, precision), round(p.y, precision))
        if coords_tuple in existing_coords:
            continue 
        
        existing_coords.add(coords_tuple)
        
        full_name = fake.name()
        email = fake.email()
        
        generated_points.append({
            "uid": uid,
            "zone": zone_id,
            "coordinates": [p.x, p.y],
            "email": email,
            "full_name": full_name
        })

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(generated_points, f, indent=2, ensure_ascii=False)

end = time.perf_counter()

print(f"{len(generated_points)} Generated points on {output_path}, time: {end - start:.6f} seconds")
