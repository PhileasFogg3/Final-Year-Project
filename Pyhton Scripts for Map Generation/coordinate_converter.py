import json

def degrees_to_dms_with_direction(deg, is_latitude):
    """
    Converts degrees to DDDMMSS format with directional prefix (N/S/E/W).
    :param deg: Degree value (float or int)
    :param is_latitude: Boolean indicating if the value is latitude
    :return: Formatted string in "DDDMMSS" with directional prefix
    """
    direction = ''
    if is_latitude:
        direction = 'N' if deg >= 0 else 'S'
    else:
        direction = 'E' if deg >= 0 else 'W'
    
    deg = abs(deg)
    d = int(deg)
    md = (deg - d) * 60
    m = int(md)
    sd = int((md - m) * 60)
    
    return f"{direction}{d:03d}{m:02d}{sd:02d}"

def convert_coordinates(coords, is_latitude=False):
    """
    Recursively converts coordinates to "DDDMMSS" format with directional prefix.
    :param coords: List of coordinates or a single coordinate pair
    :param is_latitude: Boolean indicating if the coordinate is latitude
    :return: Converted coordinates
    """
    # Single point [lon, lat]
    if isinstance(coords[0], (float, int)):
        lon = degrees_to_dms_with_direction(coords[0], is_latitude=False)
        lat = degrees_to_dms_with_direction(coords[1], is_latitude=True)
        return [lon, lat]
    # Nested coordinates (e.g., LineString, Polygon)
    elif isinstance(coords[0], list):
        return [convert_coordinates(coord) for coord in coords]
    else:
        raise ValueError(f"Unexpected coordinate format: {coords}")

# Read GEOJSON file
with open('Airspace_Boundary.geojson', 'r') as f:
    geojson_data = json.load(f)

# Iterate through features and process coordinates
for feature in geojson_data['features']:
    geometry = feature['geometry']
    geometry['coordinates'] = convert_coordinates(geometry['coordinates'])

# Write back to GEOJSON file
with open('firBoundaryConverted.geojson', 'w') as f:
    json.dump(geojson_data, f, indent=2)

print("Conversion complete. Output written to output file.")
input("Press Enter to close...")
