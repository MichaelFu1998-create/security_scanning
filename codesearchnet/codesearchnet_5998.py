def list_items(conn=None, **kwargs):
    """
    :rtype: ``list``
    """
    return [x for x in getattr( getattr( conn, kwargs.pop('service') ),
                kwargs.pop('generator'))(**kwargs)]