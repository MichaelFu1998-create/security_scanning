def collapse_initials(name):
    """Remove the space between initials, eg T. A. --> T.A."""
    if len(name.split(".")) > 1:
        name = re.sub(r'([A-Z]\.)[\s\-]+(?=[A-Z]\.)', r'\1', name)
    return name