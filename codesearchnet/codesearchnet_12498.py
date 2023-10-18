def is_ordered(cat_id):
    """
      Checks to see if a CatalogID has been ordered or not.

      Args:
        catalogID (str): The catalog ID from the platform catalog.
      Returns:
        ordered (bool): Whether or not the image has been ordered
    """
    url = 'https://rda.geobigdata.io/v1/stripMetadata/{}'.format(cat_id)
    auth = Auth()
    r = _req_with_retries(auth.gbdx_connection, url)
    if r is not None:
        return r.status_code == 200
    return False