def load_economic_data():
    global HPV_data
    if HPV_data is not None:
        return None
    global _EPACDRDict, _ECHATonnageDict
    
    '''OECD are chemicals produced by and OECD members in > 1000 tonnes/year.'''
    HPV_data = pd.read_csv(os.path.join(folder, 'HPV 2015 March 3.csv'),
                           sep='\t', index_col=0)
    # 13061-29-2 not valid and removed
    
    _ECHATonnageDict = {}
    with zipfile.ZipFile(os.path.join(folder, 'ECHA Tonnage Bands.csv.zip')) as z:
        with z.open(z.namelist()[0]) as f:
            for line in f.readlines():
                # for some reason, the file must be decoded to UTF8 first
                CAS, band = line.decode("utf-8").strip('\n').split('\t')
                if CAS in _ECHATonnageDict:
                    if band in _ECHATonnageDict[CAS]:
                        pass
                    else:
                        _ECHATonnageDict[CAS].append(band)
                else:
                    _ECHATonnageDict[CAS] = [band]
    
    
    _EPACDRDict = {}
    with open(os.path.join(folder, 'EPA 2012 Chemical Data Reporting.csv')) as f:
        '''EPA summed reported chemical usages. In metric tonnes/year after conversion.
        Many producers keep their date confidential.
        This was originally in terms of lb/year, but rounded to the nearest kg.
    
        '''
        next(f)
        for line in f:
            values = line.rstrip().split('\t')
            CAS, manufactured, imported, exported = to_num(values)
            _EPACDRDict[CAS] = {"Manufactured": manufactured/1000., "Imported": imported/1000.,
                                "Exported": exported/1000.}