def to_key(literal_or_identifier):
    ''' returns string representation of this object'''
    if literal_or_identifier['type'] == 'Identifier':
        return literal_or_identifier['name']
    elif literal_or_identifier['type'] == 'Literal':
        k = literal_or_identifier['value']
        if isinstance(k, float):
            return unicode(float_repr(k))
        elif 'regex' in literal_or_identifier:
            return compose_regex(k)
        elif isinstance(k, bool):
            return 'true' if k else 'false'
        elif k is None:
            return 'null'
        else:
            return unicode(k)