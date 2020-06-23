import numpy as np
from scipy.spatial.qhull import ConvexHull
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from osgeo import ogr


class Clusterizer(object):
    """
    This class calculates clusters from a list of geographic
    points splitting them into lists. For each cluster, non meaningful
    points are removed as well as noise
    It also calculates a convex hull for each cluster.
    """

    def __init__(self, point_list):
        """
        @param point_list: n x 2 array or numpy array representing
        lat/lon coordinates of each point. For each point, the first
        component must be longitude meanwhile, the second must be latitude
        """
        if type(point_list) is np.ndarray:
            self.points = point_list
        else:
            self.points = np.array(point_list)
        self.total_clusters = 0
        self.cluster_points = None
        self.cluster_hulls = None

    def calculate_clusters(self):
        """
        calculates and saves clusters using DBSCAN
        """
        scaler = StandardScaler()
        X = scaler.fit_transform(self.points)
        db = DBSCAN(eps=0.25, min_samples=3).fit(X)
        X = scaler.inverse_transform(X)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

        cluster_points = []
        for k in range(n_clusters_):
            class_member_mask = (labels == k)
            points_in_cluster_k = X[class_member_mask & core_samples_mask]
            cluster_points.append(points_in_cluster_k.tolist())
        self.cluster_points = cluster_points
        self.total_clusters = n_clusters_

    def plot_clusters(self):
        """
        draws cluster points. To show this you have to call Clusterizer.show_plots()
        @return:
        """
        n_clusters = self.total_clusters
        colors = [plt.cm.Spectral(each)
                  for each in np.linspace(0, 1, n_clusters)]

        for k, col in zip(range(n_clusters), colors):
            xy = np.array(self.cluster_points[k])
            plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                     markeredgecolor='k', markersize=14)

        plt.title('Estimated number of clusters: %d' % n_clusters)

    def clusters2hulls(self):
        """
        calculates a convex hull for each cluster.
        @return:
        """
        hulls = []
        n_clusters = self.total_clusters
        cluster_points = self.cluster_points
        for i in range(n_clusters):
            hull = ConvexHull(cluster_points[i])
            hulls.append(hull)
        self.cluster_hulls = hulls

    def plot_cluster_hulls(self):
        """
         draws cluster hulls. To show this you have to call Clusterizer.show_plots()
        @return:
        """
        for i in range(self.total_clusters):
            hull = self.cluster_hulls[i]
            points_in_cluster = np.array(self.cluster_points[i])
            for simplex in hull.simplices:
                plt.plot(points_in_cluster[simplex, 0], points_in_cluster[simplex, 1], 'b')

    def get_cluster_points(self):
        return self.cluster_points.copy()

    def get_cluster_hulls(self):
        return self.cluster_hulls.copy()

    def export_cluster_hulls_as_GDAL_poly(self):
        """

        @return: an array containing a GDAL polygon for each cluster
        """
        gdhulls = []
        for i in range(self.total_clusters):
            hull = self.cluster_hulls[i]
            points_in_cluster = np.array(self.cluster_points[i])
            ring = ogr.Geometry(ogr.wkbLinearRing)

            # get x and y coordinates (x and y are np.array)
            x = points_in_cluster[hull.vertices, 0]
            y = points_in_cluster[hull.vertices, 1]

            # get points
            for i in range(len(x)):
                ring.AddPoint(x[i], y[i])
            # close the polygon
            ring.AddPoint(x[0],y[0])

            poly = ogr.Geometry(ogr.wkbPolygon)
            poly.AddGeometry(ring)
            gdhulls.append(poly)
        return gdhulls


    def show_plots(self):
        plt.show()


if __name__ == '__main__':
    # Generate sample data
    from sklearn.datasets import make_blobs

    centers = [[13.39954,42.35055], [13.29924,42.35204], [13.33799,42.29093],
               [12.51133,41.89193], [13.69901,42.66123], [14.20283,42.4584]]
    X, labels_true = make_blobs(n_samples=100, centers=centers, cluster_std=0.07,
                                random_state=0)

    # use example

    cluster = Clusterizer(X)

    cluster.calculate_clusters()
    cluster.plot_clusters()


    cluster.clusters2hulls()
    cluster.plot_cluster_hulls()


    cluster.show_plots()

    hulls = cluster.get_cluster_hulls()
    points = cluster.get_cluster_points()
    gdal_hulls = cluster.export_cluster_hulls_as_GDAL_poly()
    print(points)
    print(hulls)
    for gdhull in gdal_hulls:
        print(gdhull.ExportToWkt())
        print(gdhull.IsValid())
