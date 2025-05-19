import osmnx as ox
import networkx as nx

def enrich_graph_with_travel_time(graph_path="data/processed/cluj_osm.graphml", output_path="data/processed/cluj_enriched.graphml"):
    print("Loading graph...")
    G = ox.load_graphml(graph_path)

    print("Adding edge travel times...")
    # Estimate speed in km/h and travel time in seconds
    G = ox.add_edge_speeds(G)           # Adds "speed_kph" attribute
    G = ox.add_edge_travel_times(G)     # Adds "travel_time" in seconds

    print("Saving enriched graph...")
    ox.save_graphml(G, output_path)
    print(f"Graph saved to {output_path}")

if __name__ == "__main__":
    enrich_graph_with_travel_time()
