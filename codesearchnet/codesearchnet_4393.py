def clean_attribute(attribute):
    '''
    Normalize attribute names for shorthand and work arounds for limitations
    in Python's syntax
    '''

    # Shorthand
    attribute = {
      'cls': 'class',
      'className': 'class',
      'class_name': 'class',
      'fr': 'for',
      'html_for': 'for',
      'htmlFor': 'for',
    }.get(attribute, attribute)

    # Workaround for Python's reserved words
    if attribute[0] == '_':
      attribute = attribute[1:]

    # Workaround for dash
    if attribute in set(['http_equiv']) or attribute.startswith('data_'):
      attribute = attribute.replace('_', '-').lower()

    # Workaround for colon
    if attribute.split('_')[0] in ('xlink', 'xml', 'xmlns'):
      attribute = attribute.replace('_', ':', 1).lower()

    return attribute