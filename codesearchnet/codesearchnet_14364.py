def _parse_link_header(headers):
    """Parses Github's link header for pagination.

    TODO eventually use a github client for this
    """
    links = {}
    if 'link' in headers:
        link_headers = headers['link'].split(', ')
        for link_header in link_headers:
            (url, rel) = link_header.split('; ')
            url = url[1:-1]
            rel = rel[5:-1]
            links[rel] = url
    return links