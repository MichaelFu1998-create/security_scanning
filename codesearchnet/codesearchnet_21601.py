def normalize_array(var):
    """
    Returns a normalized data array from a NetCDF4 variable. This is mostly
    used to normalize string types between py2 and py3. It has no effect on types
    other than chars/strings
    """
    if np.issubdtype(var.dtype, 'S1'):
        if var.dtype == str:
            # Python 2 on netCDF4 'string' variables needs this.
            # Python 3 returns false for np.issubdtype(var.dtype, 'S1')
            return var[:]

        def decoder(x):
            return str(x.decode('utf-8'))
        vfunc = np.vectorize(decoder)
        return vfunc(nc4.chartostring(var[:]))
    else:
        return var[:]