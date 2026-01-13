import subprocess
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

scripts = [
    "generate_customer_mockup.py",   # 1. genera los puntos aleatorios
    "enrich_customers.py",           # 2. agrega distancia y bearing
    "bearing_groups.py"              # 3. agrupa por bearing
]

for script in scripts:
    script_path = os.path.join(BASE_PATH, script)
    print(f"Running {script_path}...")
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running {script}:")
        print(result.stderr)
        break
    else:
        print(result.stdout)