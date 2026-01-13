import math

# Earth radius in meters
EARTH_RADIUS_M = 6371000


def haversine_distance(lat1, lon1, lat2, lon2, unit="meters"):
    """
    Calculate distance between two lat/lon points using Haversine formula.

    Args:
        lat1, lon1, lat2, lon2 (float): Coordinates in degrees
        unit (str): 'meters' or 'km'

    Returns:
        float: Distance between points
    """
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(
        math.radians, [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_m = EARTH_RADIUS_M * c

    if unit == "km":
        return distance_m / 1000

    return distance_m


def bearing(lat1, lon1, lat2, lon2):
    """
    Calculate bearing (direction in degrees) from point A to B.

    Returns:
        float: Bearing in degrees (0°–360°)
               0° = North, 90° = East
    """
    lat1, lat2 = map(math.radians, [lat1, lat2])
    dlon = math.radians(lon2 - lon1)

    x = math.sin(dlon) * math.cos(lat2)
    y = (
        math.cos(lat1) * math.sin(lat2)
        - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    )

    initial_bearing = math.atan2(x, y)
    bearing_deg = math.degrees(initial_bearing)

    return (bearing_deg + 360) % 360
