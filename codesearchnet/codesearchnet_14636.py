def filter_by(zips=_zips, **kwargs):
    """ Use `kwargs` to select for desired attributes from list of zipcode dicts """
    return [z for z in zips if all([k in z and z[k] == v for k, v in kwargs.items()])]