import json
import folium
import networkx as nx
from transit_graph_builder import build_transit_graph

ROUTE_TYPES = {
    0: "Tram",
    1: "Subway",
    2: "Rail",
    3: "Bus",
    4: "Ferry",
    5: "Cable Car",
    6: "Gondola",
    7: "Funicular",
    11: "Trolleybus"
}

ROUTE_COLORS = {
    3: "darkgreen",      # Bus
    11: "red",      # Trolleybus
    0: "blue",    # Tram
}

def get_stop_metadata():
    with open("data/external/stop_times.json") as f:
        stop_times = json.load(f)
    with open("data/external/trips.json") as f:
        trips = json.load(f)
    with open("data/external/routes.json") as f:
        routes = json.load(f)

    # Index trips and routes
    trip_map = {trip["trip_id"]: trip for trip in trips}
    route_map = {route["route_id"]: route for route in routes}

    # Build metadata per stop
    stop_info = {}
    for entry in stop_times:
        stop_id = entry["stop_id"]
        trip_id = entry["trip_id"]
        trip = trip_map.get(trip_id)
        if not trip:
            continue
        route = route_map.get(trip["route_id"])
        if not route:
            continue
        route_type = ROUTE_TYPES.get(route["route_type"], "Unknown")
        desc = f"{route['route_short_name']} → {trip['trip_headsign']} ({route_type})"
        stop_info.setdefault(stop_id, set()).add(desc)

    # Convert sets to readable string
    return {sid: "<br>".join(sorted(info)) for sid, info in stop_info.items()}


def get_stop_coordinates():
    with open("./data/external/stops.json") as f:
        stops = json.load(f)
    coords = {s["stop_id"]: (s["stop_lat"], s["stop_lon"]) for s in stops}
    return coords

def visualize_graph(G):
    coords = get_stop_coordinates()
    metadata = get_stop_metadata()

    m = folium.Map(location=[46.77, 23.59], zoom_start=13)

    for stop_id in G.nodes:
        lat, lon = coords[stop_id]
        popup_content = folium.Popup(metadata.get(stop_id, "No info"), max_width=250)
        folium.CircleMarker(
            location=(lat, lon),
            radius=3,
            color="blue",
            fill=True,
            fill_opacity=0.6,
            popup=popup_content
        ).add_to(m)

    for u, v, data in G.edges(data=True):
        lat1, lon1 = coords[u]
        lat2, lon2 = coords[v]
        route_type = data.get("route_type", 3)
        color = ROUTE_COLORS.get(route_type, "gray")
        folium.PolyLine(
            locations=[(lat1, lon1), (lat2, lon2)],
            color=color,
            weight=2,
            opacity=0.6
        ).add_to(m)


    m.save("output/transit_graph.html")
    print("Transit graph saved to output/transit_graph.html")


if __name__ == "__main__":
    G = build_transit_graph()
    visualize_graph(G)
