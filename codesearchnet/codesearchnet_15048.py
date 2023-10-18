def glob2re(part):
    """Convert a path part to regex syntax."""
    return "[^/]*".join(
        re.escape(bit).replace(r'\[\^', '[^').replace(r'\[', '[').replace(r'\]', ']')
        for bit in part.split("*")
    )