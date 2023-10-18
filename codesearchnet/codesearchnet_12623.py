def trim_field_key(document, field_key):
    """
    Returns the smallest delimited version of field_key that
    is an attribute on document.

    return (key, left_over_array)
    """
    trimming = True
    left_over_key_values = []
    current_key = field_key
    while trimming and current_key:
        if hasattr(document, current_key):
            trimming = False
        else:
            key_array = current_key.split("_")
            left_over_key_values.append(key_array.pop())
            current_key = u"_".join(key_array)

    left_over_key_values.reverse()
    return current_key, left_over_key_values