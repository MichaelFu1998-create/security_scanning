def parse_archive_uri(uri):
    """Given an archive URI, parse to a split ident-hash."""
    parsed = urlparse(uri)
    path = parsed.path.rstrip('/').split('/')
    ident_hash = path[-1]
    ident_hash = unquote(ident_hash)
    return ident_hash