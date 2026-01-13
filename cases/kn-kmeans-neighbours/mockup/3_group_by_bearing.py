import json
import os
import time

start = time.perf_counter()

BEARING_STEP = 5
BEARING_START = 0

INPUT_FILE = os.path.join("database", "customer_mockup.json")
OUTPUT_DIR = os.path.join("database", "bearing_groups")
os.makedirs(OUTPUT_DIR, exist_ok=True)

for file in os.listdir(OUTPUT_DIR):
    if file.endswith(".json"):
        os.remove(os.path.join(OUTPUT_DIR, file))

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    customers = json.load(f)

bearing_start = BEARING_START

while bearing_start < 365:
    end_bearing = bearing_start + BEARING_STEP
    bearing_group = []

    for idx, cust in enumerate(customers):
        bearing_cus = cust['bearing_degrees']
        bearing_group.append((bearing_cus, idx))

    filename = os.path.join(OUTPUT_DIR, f"{end_bearing}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([[c[0], c[1]] for c in bearing_group], f, indent=2, ensure_ascii=False)

    bearing_start += BEARING_STEP

end = time.perf_counter()

print(f"Finished clustering by bearing, time: {end - start:.6f} seconds")
