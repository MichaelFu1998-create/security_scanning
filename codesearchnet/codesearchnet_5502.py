def try_match(request_origin, maybe_regex):
    """Safely attempts to match a pattern or string to a request origin."""
    if isinstance(maybe_regex, RegexObject):
        return re.match(maybe_regex, request_origin)
    elif probably_regex(maybe_regex):
        return re.match(maybe_regex, request_origin, flags=re.IGNORECASE)
    else:
        try:
            return request_origin.lower() == maybe_regex.lower()
        except AttributeError:
            return request_origin == maybe_regex