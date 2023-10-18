def _gzip_sqlitecurve(sqlitecurve, force=False):
    '''This just compresses the sqlitecurve in gzip format.

    FIXME: this doesn't work with gzip < 1.6 or non-GNU gzip (probably).

    '''

    # -k to keep the input file just in case something explodes
    if force:
        cmd = 'gzip -k -f %s' % sqlitecurve
    else:
        cmd = 'gzip -k %s' % sqlitecurve

    try:

        outfile = '%s.gz' % sqlitecurve

        if os.path.exists(outfile) and not force:
            # get rid of the .sqlite file only
            os.remove(sqlitecurve)
            return outfile

        else:
            subprocess.check_output(cmd, shell=True)

            # check if the output file was successfully created
            if os.path.exists(outfile):
                return outfile
            else:
                return None

    except subprocess.CalledProcessError:
        return None