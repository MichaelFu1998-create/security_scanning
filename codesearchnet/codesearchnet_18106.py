def read_environment():
    """ Read all environment variables to see if they contain PERI """
    out = {}
    for k,v in iteritems(os.environ):
        if transform(k) in default_conf:
            out[transform(k)] = v
    return out