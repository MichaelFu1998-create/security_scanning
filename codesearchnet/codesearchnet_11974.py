def _pycompress_sqlitecurve(sqlitecurve, force=False):
    '''This just compresses the sqlitecurve. Should be independent of OS.

    '''

    outfile = '%s.gz' % sqlitecurve

    try:

        if os.path.exists(outfile) and not force:
            os.remove(sqlitecurve)
            return outfile

        else:

            with open(sqlitecurve,'rb') as infd:
                with gzip.open(outfile,'wb') as outfd:
                    shutil.copyfileobj(infd, outfd)

            if os.path.exists(outfile):
                os.remove(sqlitecurve)
                return outfile

    except Exception as e:
        return None