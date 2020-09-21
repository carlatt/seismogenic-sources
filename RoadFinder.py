
import osmnx as ox
import networkx as nx
import shapely.wkt
from pathlib import Path


class Italy_Road_Finder(object):
    def __init__(self):
        # uncomment for log console
        ox.config(use_cache=True, log_console=True)
        self.italy_gdf = ox.gdf_from_place('Italy')
        self.map = None
        self.route = None
        self.route_cache = []
        self.load_Italy()

    def load_Italy(self):
        filepath = 'data/italy.graphml'
        my_file = Path(filepath)
        if my_file.is_file():
            self.map = ox.load_graphml(filepath)
        else:
            filta = '["highway"~"motorway|motorway_link|primary"]'
            self.map = ox.graph_from_place('Italy', network_type='drive', custom_filter=filta)
            ox.save_graphml(self.map, filepath)

    def find_route(self, source, destination):
        orig = shapely.wkt.loads(source)
        dest = shapely.wkt.loads(destination)

        # Get origin x and y coordinates
        orig_xy = (orig.y, orig.x)

        # Get target x and y coordinates
        target_xy = (dest.y, dest.x)
        # Find the node in the graph that is closest to the origin point (here, we want to get the node id)
        orig_node = ox.get_nearest_node(self.map, orig_xy)

        # Find the node in the graph that is closest to the target point (here, we want to get the node id)
        target_node = ox.get_nearest_node(self.map, target_xy)

        # Calculate the shortest path
        try:
            self.route = nx.shortest_path(G=self.map, source=orig_node, target=target_node, weight='length')
        except nx.NetworkXNoPath:
            self.route = nx.shortest_path(G=self.map, source=orig_node, target=orig_node)

    def save_route(self):
        self.route_cache.append(self.route)
    def plot_route(self):
        fig, ax = ox.plot_graph_route(self.map, self.route, route_color= 'b')
    def plot_routes(self, area_of_interest):
        boundary = area_of_interest.Boundary()
        lon = []
        lat = []
        for i in range(boundary.GetPointCount()):
            x, y, not_needed = boundary.GetPoint(i)
            lon.append(x)
            lat.append(y)
        east = max(lon)+1
        west = min(lon)-1
        north = max(lat)+1
        south = min(lat)-1
        fig, ax = ox.plot_graph_routes(self.map, self.route_cache, route_color='b', route_alpha=1,  bbox=(north, south, east, west))




if __name__ == '__main__':
    map = Italy_Road_Finder()
    # Napoli -> Venezia
    map.find_route('POINT (14.26 40.86)','POINT (12.25 45.45)')
    map.plot_route()