def can_acomp(cat_id):
    """
      Checks to see if a CatalogID can be atmos. compensated or not.

      Args:
        catalogID (str): The catalog ID from the platform catalog.
      Returns:
        available (bool): Whether or not the image can be acomp'd
    """
    url = 'https://rda.geobigdata.io/v1/stripMetadata/{}/capabilities'.format(cat_id)
    auth = Auth()
    r = _req_with_retries(auth.gbdx_connection, url)
    try: 
        data = r.json()
        return data['acompVersion'] is not None
    except:
        return False