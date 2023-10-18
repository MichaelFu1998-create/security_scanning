def join_uri(uri, *segments):
    """Append segments to URI.

    Example: join_uri("/a/b", "c", "d")
    """
    sub = "/".join(segments)
    if not sub:
        return uri
    return uri.rstrip("/") + "/" + sub