from osgeo import osr, ogr

def saveGeometryAsGEOJSON(name, geom):

    fileName = 'data\geojson\\'+str(name)+'.geojson'
    # Create the output Driver
    outDriver = ogr.GetDriverByName('GeoJSON')
    outDataSource = outDriver.CreateDataSource(fileName)
    outLayer = outDataSource.CreateLayer(fileName, geom_type=geom.GetGeometryType())

    # Get the output Layer's Feature Definition
    featureDefn = outLayer.GetLayerDefn()
    # create a new feature
    outFeature = ogr.Feature(featureDefn)
    # Set new geometry
    outFeature.SetGeometry(geom)
    # Add new feature to output Layer
    outLayer.CreateFeature(outFeature)
    # dereference the feature
    outFeature = None
    # Save and close DataSources
    outDataSource = None

def saveGeometriesAsGEOJSON(name, GeometriesCollection):
    fileName = 'data\geojson\\' + str(name) + '.geojson'
    # Create the output Driver
    outDriver = ogr.GetDriverByName('GeoJSON')
    outDataSource = outDriver.CreateDataSource(fileName)
    outLayer = outDataSource.CreateLayer(fileName, geom_type=GeometriesCollection[0].GetGeometryType())

    # Get the output Layer's Feature Definition
    featureDefn = outLayer.GetLayerDefn()
    for geometry in GeometriesCollection:
        # create a new feature
        outFeature = ogr.Feature(featureDefn)
        # Set new geometry
        outFeature.SetGeometry(geometry)
        # Add new feature to output Layer
        outLayer.CreateFeature(outFeature)

    # dereference the feature
    outFeature = None
    # Save and close DataSources
    outDataSource = None

def exportAndSaveGeometryAsGEOJSON(name,geom):

    geojson = geom.ExportToJson()

    with open('data\geojson\\'+str(name)+'.geojson', 'w') as f:
        f.write(geojson)
