def _create_api_uri(self, *parts):
    """Creates fully qualified endpoint URIs.

    :param parts: the string parts that form the request URI

    """
    return urljoin(self.API_URI, '/'.join(map(quote, parts)))