def _gunzip_sqlitecurve(sqlitecurve):
    '''This just uncompresses the sqlitecurve in gzip format.

    FIXME: this doesn't work with gzip < 1.6 or non-GNU gzip (probably).

    '''

    # -k to keep the input .gz just in case something explodes
    cmd = 'gunzip -k %s' % sqlitecurve

    try:
        subprocess.check_output(cmd, shell=True)
        return sqlitecurve.replace('.gz','')
    except subprocess.CalledProcessError:
        return None