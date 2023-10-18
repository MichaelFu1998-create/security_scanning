def create_request_gfs(dateStart,dateEnd,stepList,levelList,grid,extent,paramList,typeData):
    """
        Genere la structure de requete pour le téléchargement de données GFS
        
        INPUTS:\n
        -date : au format annee-mois-jour\n
        -heure : au format heure:minute:seconde\n
        -coord : une liste des coordonnees au format [N,W,S,E]\n
        -dim_grille : taille de la grille en degree \n
    """
    
    URLlist=[]
    
    #Control datetype
    listForcastSurface=['GUST','HINDEX','PRES','HGT','TMP','WEASD','SNOD','CPOFP','WILT','FLDCP','SUNSD','LFTX','CAPE','CIN','4LFTX','HPBL','LAND']
    if (0 not in [int(x) for x in stepList]):
        listForcastSurface=listForcastSurface+['PEVPR','CPRAT','PRATE','APCP','ACPCP','WATR','CSNOW','CICEP','CFPER','CRAIN','LHTFL','SHTFL','SHTFL','GFLUX','UFLX','VFLX','U-GWD','V-GWD','DSWRF','DLWRF','ULWRF','USWRF','ALBDO']
    listAnalyseSurface=['HGT','PRES','LFTX','CAPE','CIN','4LFTX']
    
    if typeData == 'analyse' and all([x in listAnalyseSurface for x in paramList]):
        typeData= 'analyse'
        validChoice = None
        prbParameters =  None
    else:
        if all([x in listForcastSurface for x in paramList]) and typeData != 'cycleforecast':
            if typeData=='analyse':
                typeData= 'forecast'
                validChoice = typeData
            else:
                validChoice = None
            indexParameters=[i for i, elem in enumerate([x in listAnalyseSurface for x in paramList], 1) if not elem]
            prbParameters=[]
            for i in indexParameters:
                prbParameters.append(paramList[i-1])
        else:
            if typeData != 'cycleforecast':
                typeData= 'cycleforecast'
                validChoice = typeData
            else:
                validChoice = None
            indexParameters=[i for i, elem in enumerate([x in listAnalyseSurface for x in paramList], 1) if not elem]
            prbParameters=[]
            for i in indexParameters:
                prbParameters.append(paramList[i-1])
                
    #Control si date/timeList disponible
    today=date.today()
    lastData = today - timedelta(days=14)
    if dateStart < lastData or dateEnd > today : 
        exit('date are not in 14 days range from today' )
    else:
        #Pour chaque jour souhaité
        nbDays=(dateEnd-dateStart).days+1
        for i in range(0,nbDays):
            #on crontrole pour les timeList
            if dateStart + timedelta(days=i) == today:
                maxT=datetime.now().hour-5
                timeListCorr=[ x for x in stepList if x<maxT ]
            else:
                timeListCorr=stepList
              
            for t in timeListCorr:
                URL='http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_'
                #grid
                URL=URL+"{:.2f}".format(grid).replace('.','p')+'.pl?file=gfs.'
                #time ( attention limiter avec décalage horaire for today
                URL=URL+'t'+str(t).zfill(2)+'z.'
                if (grid==0.5):
                    URL=URL+'pgrb2full.'
                else:
                    URL=URL+'pgrb2.'
                URL=URL+"{:.2f}".format(grid).replace('.','p')+'.'
                
                if typeData=='cycleforecast':
                    URL=URL+'f006&lev_'
                elif typeData=='forecast':
                    URL=URL+'f000&lev_'
                else:
                    URL=URL+'anl&lev_'
                URL=URL+"=on&lev_".join(levelList)+"=on&var_"
                URL=URL+"=on&var_".join(paramList)+"=on&subregion=&"
                URL=URL+"leftlon="+str(round(float(extent[1])-0.05,1))+"&rightlon="+str(round(float(extent[3])+0.05,1))+"&toplat="+str(round(float(extent[0])+0.5,1))+"&bottomlat="+str(round(float(extent[2])-0.5,1))
                URL=URL+"&dir=%2Fgfs."+"{:%Y%m%d}".format(dateStart+timedelta(days=i))+str(t).zfill(2)
                URLlist.append(URL)
        
        return (URLlist,validChoice,prbParameters)