def similar_to(partial_zipcode, zips=_zips):
    """ List of zipcode dicts where zipcode prefix matches `partial_zipcode` """
    return [z for z in zips if z["zip_code"].startswith(partial_zipcode)]