def convertGribToTiff(listeFile,listParam,listLevel,liststep,grid,startDate,endDate,outFolder):
    """ Convert GRIB to Tif"""
    
    dicoValues={}
    
    for l in listeFile:
        grbs = pygrib.open(l)
        grbs.seek(0)
        index=1
        for j in range(len(listLevel),0,-1):
            for i in range(len(listParam)-1,-1,-1):
                grb = grbs[index]
                p=grb.name.replace(' ','_')
                if grb.level != 0:
                    l=str(grb.level)+'_'+grb.typeOfLevel
                else:
                    l=grb.typeOfLevel
                if p+'_'+l not in dicoValues.keys():
                    dicoValues[p+'_'+l]=[]
                dicoValues[p+'_'+l].append(grb.values)
                shape=grb.values.shape
                lat,lon=grb.latlons()
                geoparam=(lon.min(),lat.max(),grid,grid)
                index+= 1

    nbJour=(endDate-startDate).days+1
    #on joute des arrayNan si il manque des fichiers
    for s in range(0, (len(liststep)*nbJour-len(listeFile))):
        for k in dicoValues.keys():
            dicoValues[k].append(np.full(shape, np.nan))

    #On écrit pour chacune des variables dans un fichier
    for i in range(len(dicoValues.keys())-1,-1,-1):
        dictParam=dict((k,dicoValues[dicoValues.keys()[i]][k]) for k in range(0,len(dicoValues[dicoValues.keys()[i]])))
        sorted(dictParam.items(), key=lambda x: x[0])
        outputImg=outFolder+'/'+dicoValues.keys()[i]+'_'+startDate.strftime('%Y%M%d')+'_'+endDate.strftime('%Y%M%d')+'.tif'
        writeTiffFromDicoArray(dictParam,outputImg,shape,geoparam)
    
    for f in listeFile:
        os.remove(f)