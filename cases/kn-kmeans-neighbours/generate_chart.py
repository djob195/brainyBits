import matplotlib.pyplot as plt
import numpy as np
from utils.geo import haversine_distance
from pathlib import Path

def generate_chart(data_customers, warehouse):
    distances = []
    for client in data_customers:
        tmp = client["coordinates"]
        dist_to_point = haversine_distance(
            tmp[1], tmp[0],
            warehouse["lat"], warehouse["lon"],
            unit="meters"
        )
        distances.append(dist_to_point)
    distances.sort()

    output_path = Path("distance_increment.png")

    if output_path.exists():
        output_path.unlink()

    plt.figure(figsize=(8, 5))
    plt.plot(distances, marker='o', linestyle='-', color='blue')
    plt.title('Increment of Distances from Reference Point')
    plt.xlabel('Customer Index (sorted by distance)')
    plt.ylabel('Distance (meters)')
    plt.grid(True)

    
    plt.savefig('distance_increment.png', dpi=300)
    plt.close() 
    print("chart was generated on root project: ./distance_increment.png")

