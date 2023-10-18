def get_all_items(obj):
    """
    dict.items() but with a separate row for each value in a MultiValueDict
    """
    if hasattr(obj, 'getlist'):
        items = []
        for key in obj:
            for value in obj.getlist(key):
                items.append((key, value))
        return items
    else:
        return obj.items()