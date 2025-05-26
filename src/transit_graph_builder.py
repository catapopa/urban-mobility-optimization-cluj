import json
import networkx as nx

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def build_transit_graph():
    stops = load_json("data/external/stops.json")
    stop_times = load_json("data/external/stop_times.json")
    trips = load_json("data/external/trips.json")
    routes = load_json("data/external/routes.json")

    # Build mappings
    trip_to_route = {trip["trip_id"]: trip["route_id"] for trip in trips}
    route_to_type = {route["route_id"]: route["route_type"] for route in routes}

    G = nx.DiGraph()

    # Add nodes
    for stop in stops:
        G.add_node(
            stop["stop_id"],
            name=stop["stop_name"],
            lat=stop["stop_lat"],
            lon=stop["stop_lon"]
        )

    # Group stop_times by trip
    trip_stop_times = {}
    for entry in stop_times:
        trip_id = entry["trip_id"]
        trip_stop_times.setdefault(trip_id, []).append(entry)

    # Add edges with route_type
    for trip_id, times in trip_stop_times.items():
        times_sorted = sorted(times, key=lambda x: x["stop_sequence"])
        route_id = trip_to_route.get(trip_id)
        route_type = route_to_type.get(route_id, 3)  # Default to Bus (3) if missing

        for i in range(len(times_sorted) - 1):
            from_stop = times_sorted[i]["stop_id"]
            to_stop = times_sorted[i + 1]["stop_id"]
            G.add_edge(from_stop, to_stop, trip_id=trip_id, route_type=route_type)

    return G

if __name__ == "__main__":
    G = build_transit_graph()
    print(f"Graph built with {G.number_of_nodes()} stops and {G.number_of_edges()} connections.")
