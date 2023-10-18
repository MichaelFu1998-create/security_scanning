def convert_sav(inputfile, outputfile=None, method='rpy2', otype='csv'):
    """ Transforms the input .sav SPSS file into other format.
    If you don't specify an outputfile, it will use the
    inputfile and change its extension to .csv
    """
    assert(os.path.isfile(inputfile))
    assert(method=='rpy2' or method=='savread')

    if method == 'rpy2':
        df = sav_to_pandas_rpy2(inputfile)
    elif method == 'savread':
        df = sav_to_pandas_savreader(inputfile)

    otype_exts = {'csv': '.csv', 
                  'hdf': '.h5', 
                  'stata': '.dta',
                  'json': '.json',
                  'pickle': '.pickle',
                  'excel': '.xls',
                  'html': '.html'}

    if outputfile is None:
        outputfile = inputfile.replace(path(inputfile).ext, '')

    outputfile = add_extension_if_needed(outputfile, otype_exts[otype])

    if otype == 'csv':
        df.to_csv(outputfile)
    elif otype == 'hdf':
        df.to_hdf(outputfile, os.path.basename(outputfile))
    elif otype == 'stata':
        df.to_stata(outputfile)
    elif otype == 'json':
        df.to_json(outputfile)
    elif otype == 'pickle':
        df.to_pickle(outputfile)
    elif otype == 'excel':
        df.to_excel(outputfile)
    elif otype == 'html':
        df.to_html(outputfile)
    else:
        df.to_csv(outputfile)