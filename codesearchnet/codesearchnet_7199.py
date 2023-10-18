def markdown(tag):
    """Return start and end regex pattern sequences for simple Markdown tag."""
    return (MARKDOWN_START.format(tag=tag), MARKDOWN_END.format(tag=tag))