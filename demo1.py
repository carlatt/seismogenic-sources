import Clusterizer
import FindEmergencySources
import RoadFinder
from FindSeismogenicSources import find_seismogenic_area

if __name__ == "__main__":
    from sklearn.datasets import make_blobs
    # generate samples (representing emergency tweets) within cities.
    # samples represent coordinates within Rome, Teramo, Pescara and some neightborhoods within L'Aquila
    centers = [[13.39954, 42.35055], [13.29924, 42.35204], [13.33799, 42.29093],
               [12.51133, 41.89193], [13.69901, 42.66123], [14.20283, 42.4584]]
    X, labels_true = make_blobs(n_samples=100, centers=centers, cluster_std=0.07,
                                random_state=0)


    # actual test
    # We calculate clusters from points and export them as Polygons
    cluster = Clusterizer.Clusterizer(X)
    cluster.calculate_clusters()
    cluster.clusters2hulls()
    gdal_hulls = cluster.export_cluster_hulls_as_GDAL_poly()

    # We find the earthquake affected area
    seismogenic_area = find_seismogenic_area(gdal_hulls, 6)
    emergency_area = FindEmergencySources.find_emergency_area(seismogenic_area)

    # We find province capitals near earthquake affected (emergency) area from where
    # rescues come from
    capitals = FindEmergencySources.find_emergency_sources(emergency_area)

    # We load a map of Italy containing highways and primary roads
    map = RoadFinder.Italy_Road_Finder()

    # we find and then plot the shortest path from capital cities to the emergency area centroid
    for capital in capitals:
        source = capital.Centroid()
        destination = emergency_area.Centroid()
        map.find_route(source.ExportToWkt(), destination.ExportToWkt())
        map.plot_route()

