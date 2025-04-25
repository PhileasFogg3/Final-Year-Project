import requests
import csv
import time
from datetime import datetime, timedelta

# FlightAware API credentials
API_KEY = "API KEY REMOVED FOR PRIVACY"
BASE_URL = "https://aeroapi.flightaware.com/aeroapi"

# Define the bounding box for the region (North Atlantic example)
NORTH_LAT = 65.0   # Northernmost latitude
SOUTH_LAT = 30.0   # Southernmost latitude
WEST_LON = -70.0   # Westernmost longitude
EAST_LON = -10.0   # Easternmost longitude

# Run the script for 24 hours (once per hour)
TOTAL_RUNS = 24
INTERVAL = 3600  # 1 hour in seconds

def get_flights():
    """Fetch flights within a specific latitude/longitude bounding box."""
    flights_data = []
    headers = {"x-apikey": API_KEY}

    url = f"{BASE_URL}/flights/search"

    # Correctly formatted lat/long query
    query = f'-latlong "{NORTH_LAT} {WEST_LON} {SOUTH_LAT} {EAST_LON}"'

    params = {"query": query, "max_pages": 10}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        flights = response.json().get("flights", [])

        for flight in flights:
            callsign = flight.get("ident", "N/A")
            aircraft_type = flight.get("aircraft_type", "N/A")

            # Safe extraction of departure airport ICAO code
            departure_airport = flight.get("origin", {}).get("code_icao", "Unknown")

            # Safe extraction of destination airport ICAO code
            if flight.get("destination"):
                destination_airport = flight["destination"].get("code_icao", "Unknown")
            else:
                destination_airport = "Unknown"

            # Extract and format departure time (if available)
            departure_time = flight.get("actual_departure_time", "N/A")
            if departure_time != "N/A":
                departure_time = datetime.utcfromtimestamp(departure_time).strftime("%Y-%m-%d %H:%M:%S")

            # Append cleaned data
            flights_data.append([callsign, aircraft_type, departure_airport, destination_airport, departure_time])

    except requests.exceptions.RequestException as e:
        print(f"Error fetching flight data: {e}")

    return flights_data


def save_to_csv(flights, timestamp):
    """Saves flight data to a uniquely named CSV file."""
    filename = f"flights_log_{timestamp}.csv"

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Callsign", "Aircraft Type", "Departure", "Destination", "Departure Time (UTC)"])
        writer.writerows(flights)

    print(f"Flight data saved to {filename}")


def main():
    """Runs the flight data collection every hour for 24 hours."""
    for i in range(TOTAL_RUNS):
        print(f"Fetching flight data... Run {i+1} of {TOTAL_RUNS}")

        flights = get_flights()

        if not flights:
            print("No flights found in the specified region.")
        else:
            # Generate timestamped filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            save_to_csv(flights, timestamp)

        if i < TOTAL_RUNS - 1:  # Don't sleep after the last run
            print("Waiting for 1 hour before next run...\n")
            time.sleep(INTERVAL)  # Wait for 1 hour

    print("Completed 24-hour flight recording.")


if __name__ == "__main__":
    main()
