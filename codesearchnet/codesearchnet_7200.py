def html(tag):
    """Return sequence of start and end regex patterns for simple HTML tag"""
    return (HTML_START.format(tag=tag), HTML_END.format(tag=tag))