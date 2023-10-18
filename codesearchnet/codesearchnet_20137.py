def convertShpToExtend(pathToShp):
    """
    reprojette en WGS84 et recupere l'extend
    """ 
    
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataset = driver.Open(pathToShp)
    if dataset is not None:
        # from Layer
        layer = dataset.GetLayer()
        spatialRef = layer.GetSpatialRef()
        # from Geometry
        feature = layer.GetNextFeature()
        geom = feature.GetGeometryRef()
        spatialRef = geom.GetSpatialReference()
        
        #WGS84
        outSpatialRef = osr.SpatialReference()
        outSpatialRef.ImportFromEPSG(4326)

        coordTrans = osr.CoordinateTransformation(spatialRef, outSpatialRef)

        env = geom.GetEnvelope()

        pointMAX = ogr.Geometry(ogr.wkbPoint)
        pointMAX.AddPoint(env[1], env[3])
        pointMAX.Transform(coordTrans)
        
        pointMIN = ogr.Geometry(ogr.wkbPoint)
        pointMIN.AddPoint(env[0], env[2])
        pointMIN.Transform(coordTrans)


        return [pointMAX.GetPoint()[1],pointMIN.GetPoint()[0],pointMIN.GetPoint()[1],pointMAX.GetPoint()[0]]
    else:
        exit(" shapefile not found. Please verify your path to the shapefile")