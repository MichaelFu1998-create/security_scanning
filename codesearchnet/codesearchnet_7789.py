def less_than_version(value):
    """
    Converts the current version to the next one for inserting into requirements
    in the ' < version' format
    """
    items = list(map(int, str(value).split('.')))
    if len(items) == 1:
        items.append(0)
    items[1] += 1
    if value == '1.11':
        return '2.0'
    else:
        return '.'.join(map(str, items))