import osmnx as ox
import networkx as nx

ox.settings.overpass_endpoint = "https://overpass.kumi.systems/api/interpreter"

def download_osm_graph(place="Cluj-Napoca, Romania"):
    """
    Downloads the drivable street network for Cluj-Napoca.
    """
    print(f"Downloading road network for {place}...")
    G = ox.graph_from_place(place, network_type='drive')
    return G

if __name__ == "__main__":
    G = download_osm_graph()
    ox.save_graphml(G, filepath="data/processed/cluj_osm.graphml")
    print("Graph downloaded and saved.")
