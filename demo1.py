import Clusterizer
import FindEmergencySources
import RoadFinder
from FindEmergencySources import *

if __name__ == "__main__":
    from sklearn.datasets import make_blobs
    # generate samples (representing emergency tweets) within cities.
    # samples represent coordinates within Rome, Teramo, Pescara and  L'Aquila
    centers = [[13.33799, 42.29093],
               [12.51133, 41.89193], [13.69901, 42.66123], [14.20283, 42.4584]]
    X, labels_true = make_blobs(n_samples=20, centers=centers, cluster_std=0.5,
                                random_state=0)


    # actual test
    # We calculate clusters from points and export them as Polygons
    cluster = Clusterizer.Clusterizer(X)
    cluster.calculate_clusters()
    cluster.clusters2hulls()
    gdal_hulls = cluster.export_cluster_hulls_as_GDAL_poly()

    # We find the earthquake affected area
    nSources = 6  # number of possible sources

    SeismSources = SeismogenicSources(gdal_hulls, nSources)
    seismogenic_area = SeismSources.findedArea

    SeismSources.plot_seismogenic_data(plotItaly=True)
    plt.savefig('seismogenicSources')
    plt.show()

    EmergSources = EmergencySources(seismogenic_area)
    emergency_area = EmergSources.emergencyArea

    EmergSources.plot_emergency_data(plotItaly=True)
    plt.savefig('emergencySources')
    plt.show()

    # We find province capitals near earthquake affected (emergency) area from where
    # rescues come from
    capitals = EmergSources.emergencySources



    # We load a map of Italy containing highways and primary roads
    map = RoadFinder.Italy_Road_Finder()

    # we find and then plot the shortest path from capital cities to the emergency area centroid
    for capital in capitals:
        source = capital.Centroid()
        destination = emergency_area.Centroid()
        map.find_route(source.ExportToWkt(), destination.ExportToWkt())
        map.save_route()
        #map.plot_route()
    map.plot_routes()
    
