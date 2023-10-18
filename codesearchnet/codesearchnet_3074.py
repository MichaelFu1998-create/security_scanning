def trans(ele, standard=False):
    """Translates esprima syntax tree to python by delegating to appropriate translating node"""
    try:
        node = globals().get(ele['type'])
        if not node:
            raise NotImplementedError('%s is not supported!' % ele['type'])
        if standard:
            node = node.__dict__[
                'standard'] if 'standard' in node.__dict__ else node
        return node(**ele)
    except:
        #print ele
        raise