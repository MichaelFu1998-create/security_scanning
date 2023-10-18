def parse(svg, cached=False, _copy=True):
    
    """ Returns cached copies unless otherwise specified.
    """
    
    if not cached:
        dom = parser.parseString(svg)
        paths = parse_node(dom, [])
    else:
        id = _cache.id(svg)
        if not _cache.has_key(id):
            dom = parser.parseString(svg)
            _cache.save(id, parse_node(dom, []))
        paths = _cache.load(id, _copy)
   
    return paths