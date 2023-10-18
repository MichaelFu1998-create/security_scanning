def parse_query(query):
    """
    Given a simplified XPath query string, returns an array of normalized query parts.
    """
    parts = query.split('/')
    norm = []
    for p in parts:
        p = p.strip()
        if p:
            norm.append(p)
        elif '' not in norm:
            norm.append('')
    return norm