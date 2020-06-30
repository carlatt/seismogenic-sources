from osgeo import osr, ogr
from visuallayer import *

def find_candidate_sources(polygons):
    # load the composite seismologic sources from the shapefile 'CSSPLN321.shp''
    driver = ogr.GetDriverByName("ESRI Shapefile")
    file_seism = 'data/INGV/ISS321.shp'
    vector_seism = driver.Open(file_seism, 0)
    layer_seism = vector_seism.GetLayer(0)

    # Find nearest seismologic sources for each area (e.g. with dist of 20 km)
    candidatesCount = {}
    candidates =[]
    for polygon in polygons:
        sources = find_nearest_sources(polygon,layer_seism)
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
    plt.show()
    return sortedCandidatesCount, candidates

def find_nearest_sources(polygon,layer_seism):

    area = polygon.Buffer(1)

    plot_geometry(polygon, fillcolor='green', alpha=1)
    plot_geometry(area, fillcolor='grey', alpha=0.2)
    sources=[]
    for source in layer_seism:
        source_geom = source.GetGeometryRef().GetGeometryRef(0)
        source_poly = ogr.Geometry(ogr.wkbPolygon)
        source_poly.AddGeometry(source_geom)
        #plot_geometry(source_poly, fillcolor='blue', alpha=0.2)

        if area.Intersects(source_poly):
            sources.append(source)
            plot_geometry(source_poly, fillcolor='blue', alpha=0.2)

    return sources

def find_affected_area(polygons):
    candidatesCount, candidates = find_candidate_sources(polygons)

    union = ogr.Geometry(ogr.wkbPolygon)
    #find a 15km buffer for each candidate and dothe union of them
    for candidate in candidates:
        plot_geometry(candidate, fillcolor='blue', alpha=1)
        union = union.Union(candidate.Buffer(1))

    print (union)
    plot_geometry(union, fillcolor='grey', alpha=0.5)
    plt.show()


if __name__ == '__main__':

    p1='POLYGON((13.5068345450051 42.453405113893 0, 13.4096230499813 42.4523491454874 0, 13.2115443247965 42.4064643249082 0, 13.1851261157124 42.3844347578868 0, 13.1862671506709 42.337148180385 0, 13.2258412924453 42.2526387443975 0, 13.2423197602569 42.2312002178368 0, 13.3705863707811 42.1833929419606 0, 13.4698105487939 42.19658686572 0, 13.5302690593105 42.2821405484086 0, 13.5230236642177 42.3785610045857 0, 13.5068345450051 42.453405113893 0))'
    p2='POLYGON((14.2465962015719 42.3462559641075 0, 14.2859920854647 42.4805859828347 0, 14.256855338585 42.5160452907775 0, 14.1304330010751 42.5061116162797 0, 14.1123300163194 42.4770935608544 0, 14.1465913235078 42.4101315155575 0, 14.1780504262123 42.3621534094607 0, 14.2465962015719 42.3462559641075 0))'
    p3='POLYGON((12.422396050106 41.9597877695711 0, 12.4823766713468 41.8396081631992 0, 12.5776376377442 41.8810792934836 0, 12.6420591272299 41.9553531260793 0, 12.6459359418536 41.9955660354004 0, 12.4808692513795 42.0213784609936 0, 12.4510442020462 42.0256345467169 0, 12.429211361642 42.0279834829955 0, 12.422396050106 41.9597877695711 0))'
    p4='POLYGON((13.6289949256827 42.5530960232256 0, 13.7778745145475 42.5856347944146 0, 13.7654694564848 42.667358586897 0, 13.6942330876273 42.7811639905155 0, 13.6351124442189 42.7394211401667 0, 13.6132295136819 42.7203354083481 0, 13.5946219685106 42.6919874190885 0, 13.6068964812642 42.628919077663 0, 13.6289949256827 42.5530960232256 0))'

    polygon1 = ogr.CreateGeometryFromWkt(p1)
    polygon2 = ogr.CreateGeometryFromWkt(p2)
    polygon3 = ogr.CreateGeometryFromWkt(p3)
    polygon4 = ogr.CreateGeometryFromWkt(p4)
    polygons=[polygon1,polygon2,polygon3,polygon4]

    #candidatesCount, candidates = find_candidate_sources(polygons)
    #print (candidatesCount)
    find_affected_area(polygons)



