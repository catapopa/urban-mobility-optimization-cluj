import requests
import json
import os

TRANZY_API_KEY = "api_key"  # Replace with your actual API key
BASE_URL = "https://api.tranzy.ai/v1/opendata"
AGENCY_ID = "2"  

HEADERS = {
    "accept": "application/json",
    "X-API-KEY": TRANZY_API_KEY,
    "X-Agency-Id": AGENCY_ID
}


def fetch_gtfs_data():
    os.makedirs("data/external", exist_ok=True)

    print("Fetching routes...")
    routes = requests.get(f"{BASE_URL}/routes", headers=HEADERS).json()
    with open("data/external/routes.json", "w") as f:
        json.dump(routes, f)

    print("Fetching stops...")
    stops = requests.get(f"{BASE_URL}/stops", headers=HEADERS).json()
    with open("data/external/stops.json", "w") as f:
        json.dump(stops, f)

    print("Fetching shapes...")
    shapes = requests.get(f"{BASE_URL}/shapes", headers=HEADERS).json()
    with open("data/external/shapes.json", "w") as f:
        json.dump(shapes, f)

    print("Fetching trips...")
    routes = requests.get(f"{BASE_URL}/trips", headers=HEADERS).json()
    with open("data/external/trips.json", "w") as f:
        json.dump(routes, f)

    print("Fetching stop times...")
    routes = requests.get(f"{BASE_URL}/stop_times", headers=HEADERS).json()
    with open("data/external/stop_times.json", "w") as f:
        json.dump(routes, f)

    print("GTFS data saved.")

if __name__ == "__main__":
    fetch_gtfs_data()
