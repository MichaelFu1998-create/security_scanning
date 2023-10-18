def strip_html_tags(text, allowed_tags=None):
    """
    Strip all tags from a string except those tags provided in `allowed_tags` parameter.

    Args:
        text (str): string to strip html tags from
        allowed_tags (list): allowed list of html tags

    Returns: a string without html tags
    """
    if text is None:
        return
    if allowed_tags is None:
        allowed_tags = ALLOWED_TAGS
    return bleach.clean(text, tags=allowed_tags, attributes=['id', 'class', 'style', 'href', 'title'], strip=True)