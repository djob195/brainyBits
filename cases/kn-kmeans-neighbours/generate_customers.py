import sys
import os
import runpy

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
if BASE_PATH not in sys.path:
    sys.path.insert(0, BASE_PATH)

MOCKUP_DIR = os.path.join(BASE_PATH, "mockup")

SCRIPTS = [
    "1_customers_generator.py",
    "2_enrich_customers.py",
    "3_group_by_bearing.py",
]

for script_name in SCRIPTS:
    script_path = os.path.join(MOCKUP_DIR, script_name)
    if not os.path.exists(script_path):
        print(f"Script not found: {script_path}")
        continue

    print(f"\n--- Running {script_name} ---")
    runpy.run_path(script_path, run_name="__main__")
    print(f"--- Finished {script_name} ---\n")
