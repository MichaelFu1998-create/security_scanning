def _pyuncompress_sqlitecurve(sqlitecurve, force=False):
    '''This just uncompresses the sqlitecurve. Should be independent of OS.

    '''

    outfile = sqlitecurve.replace('.gz','')

    try:

        if os.path.exists(outfile) and not force:
            return outfile

        else:

            with gzip.open(sqlitecurve,'rb') as infd:
                with open(outfile,'wb') as outfd:
                    shutil.copyfileobj(infd, outfd)

            # do not remove the intput file yet
            if os.path.exists(outfile):
                return outfile

    except Exception as e:
        return None