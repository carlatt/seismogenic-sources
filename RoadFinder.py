
import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import shapely.wkt


class Road_Finder(object):
    def __init__(self,bounding_wkt_poly):
        self.filter = '["highway"~"motorway|motorway_link|primary|secondary|tertiary"]'
        self.bounding_area = None
        self.set_bounding_area(bounding_wkt_poly)
        self.route = None

    def set_bounding_area(self, bounding_wkt_poly):
        poly = shapely.wkt.loads(bounding_wkt_poly)
        bound_graph = ox.graph_from_polygon(poly, network_type='drive',
                                      custom_filter=self.filter)
        self.bounding_area = ox.project_graph(bound_graph)
    def find_route(self, source, destination):
        orig = shapely.wkt.loads(source)
        dest = shapely.wkt.loads(destination)

        # Get origin x and y coordinates
        orig_xy = (orig.y, orig.x)

        # Get target x and y coordinates
        target_xy = (dest.y, dest.x)
        # Find the node in the graph that is closest to the origin point (here, we want to get the node id)
        orig_node = ox.get_nearest_node(self.bounding_area, orig_xy, method='euclidean')

        # Find the node in the graph that is closest to the target point (here, we want to get the node id)
        target_node = ox.get_nearest_node(self.bounding_area, target_xy, method='euclidean')

        # Calculate the shortest path
        self.route = nx.shortest_path(G=self.bounding_area, source=orig_node, target=target_node, weight='length')

    def plot_route(self):
        fig, ax = ox.plot_graph_route(self.bounding_area, self.route)

if __name__ == '__main__':
    map = Road_Finder('POLYGON ((13.6289949256827 42.5530960232256 0,13.7778745145475 42.5856347944146 0,13.7654694564848 42.667358586897 0,13.6942330876273 42.7811639905155 0,13.6351124442189 42.7394211401667 0,13.6132295136819 42.7203354083481 0,13.5946219685106 42.6919874190885 0,13.6068964812642 42.628919077663 0,13.6289949256827 42.5530960232256 0))')
    map.find_route('POINT (392251.0703174342 4723469.37369192)','POINT (387778.4110260574 4712421.508545556)')
    map.plot_route()