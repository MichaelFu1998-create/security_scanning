def read_hatpi_textlc(lcfile):
    '''
    This reads in a textlc that is complete up to the TFA stage.

    '''

    if 'TF1' in lcfile:
        thiscoldefs = COLDEFS + [('itf1',float)]
    elif 'TF2' in lcfile:
        thiscoldefs = COLDEFS + [('itf2',float)]
    elif 'TF3' in lcfile:
        thiscoldefs = COLDEFS + [('itf3',float)]

    LOGINFO('reading %s' % lcfile)

    if lcfile.endswith('.gz'):
        infd = gzip.open(lcfile,'r')
    else:
        infd = open(lcfile,'r')


    with infd:

        lclines = infd.read().decode().split('\n')
        lclines = [x.split() for x in lclines if ('#' not in x and len(x) > 0)]
        ndet = len(lclines)

        if ndet > 0:

            lccols = list(zip(*lclines))
            lcdict = {x[0]:y for (x,y) in zip(thiscoldefs, lccols)}

            # convert to ndarray
            for col in thiscoldefs:
                lcdict[col[0]] = np.array([col[1](x) for x in lcdict[col[0]]])

        else:

            lcdict = {}
            LOGWARNING('no detections in %s' % lcfile)
            # convert to empty ndarrays
            for col in thiscoldefs:
                lcdict[col[0]] = np.array([])

        # add the object's name to the lcdict
        hatid = HATIDREGEX.findall(lcfile)
        lcdict['objectid'] = hatid[0] if hatid else 'unknown object'

        # add the columns to the lcdict
        lcdict['columns'] = [x[0] for x in thiscoldefs]

        # add some basic info similar to usual HATLCs
        lcdict['objectinfo'] = {
            'ndet':ndet,
            'hatid':hatid[0] if hatid else 'unknown object',
            'network':'HP',
        }

        # break out the {stationid}-{framenum}{framesub}_{ccdnum} framekey
        # into separate columns
        framekeyelems = FRAMEREGEX.findall('\n'.join(lcdict['frk']))

        lcdict['stf'] = np.array([(int(x[0]) if x[0].isdigit() else np.nan)
                                  for x in framekeyelems])
        lcdict['cfn'] = np.array([(int(x[1]) if x[0].isdigit() else np.nan)
                                  for x in framekeyelems])
        lcdict['cfs'] = np.array([x[2] for x in framekeyelems])
        lcdict['ccd'] = np.array([(int(x[3]) if x[0].isdigit() else np.nan)
                                  for x in framekeyelems])

        # update the column list with these columns
        lcdict['columns'].extend(['stf','cfn','cfs','ccd'])

        # add more objectinfo: 'stations', etc.
        lcdict['objectinfo']['network'] = 'HP'
        lcdict['objectinfo']['stations'] = [
            'HP%s' % x for x in np.unique(lcdict['stf']).tolist()
        ]


    return lcdict