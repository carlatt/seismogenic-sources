from osgeo import osr, ogr
from visuallayer import *
from utils import *

class SeismogenicSources:
    def __init__(self, clusters, nSources):
        self.clusters = clusters
        self.numberOfSources = nSources
        self.clustersBuffer = 0.7
        self.faultsBuffer = 0.3
        self.foundSources = self.find_n_candidate_sources(clusters, nSources)
        self.foundArea = self.find_seismogenic_area(clusters, nSources)
        self.areaOfInterest= self.find_area_of_interest()
        self.foundCities = self.find_cities_at_risk()

    def find_candidate_sources(self, polygons):
        # load the composite seismologic sources from the shapefile 'CSSPLN321.shp''
        driver = ogr.GetDriverByName("ESRI Shapefile")
        file_seism = 'data/INGV/ISS321.shp'
        vector_seism = driver.Open(file_seism, 0)
        layer_seism = vector_seism.GetLayer(0)

        # Find nearest seismologic sources for each area (e.g. with dist of 20 km)
        candidatesCount = {}
        candidates =[]
        for polygon in polygons:
            sources = self.find_nearest_sources(polygon,layer_seism)
            for source in sources:
                sourceID = source.GetField(0)
                if sourceID in candidatesCount:
                    candidatesCount[sourceID]=candidatesCount[sourceID]+1
                else:
                    candidatesCount[sourceID]=1
                    source_geom = source.GetGeometryRef().GetGeometryRef(0)
                    source_poly = ogr.Geometry(ogr.wkbPolygon)
                    source_poly.AddGeometry(source_geom)
                    candidates.append(source_poly)


        sortedCandidatesCount = sorted(candidatesCount.items(), key=lambda x: x[1], reverse=True)
        return sortedCandidatesCount, candidates

    def find_n_candidate_sources(self, polygons, n):
        candidatesCount, candidates = self.find_candidate_sources(polygons)
        n_candidates = []
        for i in range(0, min(n,len(candidatesCount))):
            n_candidates.append(candidates[i])
        saveGeometriesAsGEOJSON('seismogenicSources', n_candidates)
        return  n_candidates

    def find_nearest_sources(self, polygon,layer_seism):

        area = polygon.Buffer(self.clustersBuffer)

        sources=[]
        for source in layer_seism:
            source_geom = source.GetGeometryRef().GetGeometryRef(0)
            source_poly = ogr.Geometry(ogr.wkbPolygon)
            source_poly.AddGeometry(source_geom)

            if area.Intersects(source_poly):
                sources.append(source)

        return sources

    def find_seismogenic_area(self, polygons,n):

        candidates = self.find_n_candidate_sources(polygons, n)
        union = ogr.Geometry(ogr.wkbPolygon)

        #find a 15km buffer for each candidate and do the union of them
        for candidate in candidates:
            union = union.Union(candidate.Buffer(self.faultsBuffer))
        saveGeometryAsGEOJSON('areaAtRisk',union)
        centroid = union.Centroid()
        #saveGeometryAsFeatureGEOJSON('centroid_areaatrisk', centroid)
        return union

    def find_cities_at_risk(self):
        return 1
        #Todo: finire que

    def find_area_of_interest(self):
        area_of_interest = ogr.Geometry(ogr.wkbPolygon)
        for source in self.foundSources:
            area_of_interest = area_of_interest.Union(source)
        area_of_interest = area_of_interest.Union(self.foundArea)
        return area_of_interest

    def plot_seismogenic_data(self, plotItaly):
        if (plotItaly == True):
            #plot italy in the area of interest
            plot_italy(self.areaOfInterest)

        #plot clusters
        for cluster in self.clusters:
            plot_geometry(cluster, fillcolor='green', alpha=1)
            plot_geometry(cluster.Buffer(self.clustersBuffer), fillcolor='grey', alpha=0.2)

        #plot the possible seismogenic area
        plot_geometry(self.foundArea, fillcolor='red', alpha=0.1)

        #plot the first n possible seismogenic source
        for source in self.foundSources:
            plot_geometry(source, fillcolor='blue', alpha=0.5)

def plot_italy(area_of_interest):
    envelope = get_envelope_as_geometry(area_of_interest.Buffer(0.3))
    ds = ogr.Open('data')  # file name and path
    layer = ds.GetLayer('ne_50m_admin_0_countries')
    layer.SetAttributeFilter("name = 'Italy'")  # there is only one feature in the layer with this condition!
    feature = layer.GetNextFeature()  # therefore, we are importing Germany

    italy_geom=feature.GetGeometryRef()
    intersection = italy_geom.Intersection(envelope)

    plot_geometry(intersection, fillcolor='gold', alpha=0.5)

def get_envelope_as_geometry(geom):
    (minX, maxX, minY, maxY) = geom.GetEnvelope()
    # Create ring
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(minX, minY)
    ring.AddPoint(maxX, minY)
    ring.AddPoint(maxX, maxY)
    ring.AddPoint(minX, maxY)
    ring.AddPoint(minX, minY)
    # Create polygon
    poly_envelope = ogr.Geometry(ogr.wkbPolygon)
    poly_envelope.AddGeometry(ring)

    return poly_envelope


if __name__ == '__main__':

    p1='POLYGON((13.5068345450051 42.453405113893 0, 13.4096230499813 42.4523491454874 0, 13.2115443247965 42.4064643249082 0, 13.1851261157124 42.3844347578868 0, 13.1862671506709 42.337148180385 0, 13.2258412924453 42.2526387443975 0, 13.2423197602569 42.2312002178368 0, 13.3705863707811 42.1833929419606 0, 13.4698105487939 42.19658686572 0, 13.5302690593105 42.2821405484086 0, 13.5230236642177 42.3785610045857 0, 13.5068345450051 42.453405113893 0))'
    p2='POLYGON((14.2465962015719 42.3462559641075 0, 14.2859920854647 42.4805859828347 0, 14.256855338585 42.5160452907775 0, 14.1304330010751 42.5061116162797 0, 14.1123300163194 42.4770935608544 0, 14.1465913235078 42.4101315155575 0, 14.1780504262123 42.3621534094607 0, 14.2465962015719 42.3462559641075 0))'
    p3='POLYGON((12.422396050106 41.9597877695711 0, 12.4823766713468 41.8396081631992 0, 12.5776376377442 41.8810792934836 0, 12.6420591272299 41.9553531260793 0, 12.6459359418536 41.9955660354004 0, 12.4808692513795 42.0213784609936 0, 12.4510442020462 42.0256345467169 0, 12.429211361642 42.0279834829955 0, 12.422396050106 41.9597877695711 0))'
    p4='POLYGON((13.6289949256827 42.5530960232256 0, 13.7778745145475 42.5856347944146 0, 13.7654694564848 42.667358586897 0, 13.6942330876273 42.7811639905155 0, 13.6351124442189 42.7394211401667 0, 13.6132295136819 42.7203354083481 0, 13.5946219685106 42.6919874190885 0, 13.6068964812642 42.628919077663 0, 13.6289949256827 42.5530960232256 0))'

    polygon1 = ogr.CreateGeometryFromWkt(p1)
    polygon2 = ogr.CreateGeometryFromWkt(p2)
    polygon3 = ogr.CreateGeometryFromWkt(p3)
    polygon4 = ogr.CreateGeometryFromWkt(p4)
    clusters=[polygon1,polygon2,polygon3,polygon4]

    nSources= 3 #number of possible sources

    SeismSources = SeismogenicSources(clusters, nSources)

    print(SeismSources.foundSources)
    print(SeismSources.foundArea)

    SeismSources.plot_seismogenic_data(plotItaly=True)
    plt.savefig('seismogenicSources')
    plt.show()

