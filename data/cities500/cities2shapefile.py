from osgeo import ogr, osr

def cityStr2Dict(cityStr):
    city = (cityStr.rstrip()).split('\t')
    return {
        'geonameid': city[0],
        'name': city[1],
        'asciiname': city[2],
        'alternatenames': city[3],
        'latitude': city[4],
        'longitude': city[5],
        'feature class': city[6],
        'feature code': city[7],
        'country code': city[8],
        'cc2': city[9],
        'admin1 code': city[10],
        'admin2 code': city[11],
        'admin3 code': city[12],
        'admin4 code': city[13],
        'population': city[14],
        'elevation': city[15],
        'dem': city[16],
        'timezone': city[17],
        'modification date': city[18],
    }



if __name__ == '__main__':

    path = './cities500_IT.shp'
    drvName = "ESRI Shapefile"
    driver = ogr.GetDriverByName(drvName)

    shapeData = driver.CreateDataSource(path)
    spatialReference = osr.SpatialReference()
    spatialReference.ImportFromEPSG(4326)
    layer = shapeData.CreateLayer('cities', spatialReference, ogr.wkbPoint)
    layer_defn = layer.GetLayerDefn()
    new_field = ogr.FieldDefn('name', ogr.OFTString)  # we will create a new field called Hometown as String
    layer.CreateField(new_field)  # self explaining
    new_field = ogr.FieldDefn('population', ogr.OFTString)  # we will create a new field called Hometown as String
    layer.CreateField(new_field)  # self explaining
    new_field = ogr.FieldDefn('code', ogr.OFTString)  # we will create a new field called Hometown as String
    layer.CreateField(new_field)  # self explaining
    new_field = ogr.FieldDefn('province', ogr.OFTString)  # we will create a new field called Hometown as String
    layer.CreateField(new_field)  # self explaining

    i=0
    with open('cities500.txt', 'r', encoding='utf') as f:
        lines = f.readlines()
        for line in lines:
            city = cityStr2Dict(line)
            if city['country code'] == 'IT':
                point = ogr.CreateGeometryFromWkt(
                    "POINT({} {})".format(city['longitude'], city['latitude']))
                featureIndex = i
                feature = ogr.Feature(layer_defn)
                feature.SetGeometry(point)
                feature.SetFID(featureIndex)

                layer.CreateFeature(feature)

                feature = layer.GetFeature(i)
                name = feature.GetFieldIndex("name")
                population = feature.GetFieldIndex("population")
                feature_code = feature.GetFieldIndex("code")
                province = feature.GetFieldIndex("province")
                feature.SetField(name, city['name'])
                feature.SetField(population, city['population'])
                feature.SetField(feature_code, city['feature code'])
                feature.SetField(province, city['admin2 code'])
                layer.SetFeature(feature)
                print(city['name'])
                i=i+1
    shapeData.Destroy()

