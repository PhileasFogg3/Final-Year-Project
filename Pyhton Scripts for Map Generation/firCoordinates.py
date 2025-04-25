import json

# Function to convert coordinate string to lat/lon
# N/S for latitude, E/W for longitude
def parse_coordinate(coord):
    return coord

def convert_geojson_to_xml(input_file, output_file):
    # Load JSON data
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    # Initialize the output XML content
    output_lines = ["<?xml version=\"1.0\" encoding=\"UTF-8\"?>"]

    for feature in data.get("features", []):
        output_lines.append("<path>")
        
        # Extract name
        name = feature.get("properties", {}).get("NAME", "Unknown")
        output_lines.append(f"    <name>{name}</name>")
        
        # Extract coordinates
        coordinates = feature.get("geometry", {}).get("coordinates", [])
        for line in coordinates:
            for coord_pair in line:
                lat = parse_coordinate(coord_pair[1])
                lon = parse_coordinate(coord_pair[0])

                if lat is not None and lon is not None:
                    output_lines.append(f"    <point lat=\"{lat}\" lon=\"{lon}\"/>")

        output_lines.append("</path>")

    # Write the output to file
    with open(output_file, 'w') as outfile:
        outfile.write("\n".join(output_lines))

# Example usage
convert_geojson_to_xml('firBoundaryConverted.geojson', 'firBoundaryMap.xml')

print("Conversion complete. Output written to output file.")
input("Press Enter to close...")