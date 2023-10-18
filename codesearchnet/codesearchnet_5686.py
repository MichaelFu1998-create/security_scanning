def _redirect_with_params(url_name, *args, **kwargs):
    """Helper method to create a redirect response with URL params.

    This builds a redirect string that converts kwargs into a
    query string.

    Args:
        url_name: The name of the url to redirect to.
        kwargs: the query string param and their values to build.

    Returns:
        A properly formatted redirect string.
    """
    url = urlresolvers.reverse(url_name, args=args)
    params = parse.urlencode(kwargs, True)
    return "{0}?{1}".format(url, params)