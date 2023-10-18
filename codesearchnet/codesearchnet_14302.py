def clean_empty_string(obj):
    """
    Replace empty form values with None, since the is_html_input() check in
    Field won't work after we convert to JSON.
    (FIXME: What about allow_blank=True?)
    """
    if obj == '':
        return None
    if isinstance(obj, list):
        return [
            None if item == '' else item
            for item in obj
        ]
    if isinstance(obj, dict):
        for key in obj:
            obj[key] = clean_empty_string(obj[key])
    return obj