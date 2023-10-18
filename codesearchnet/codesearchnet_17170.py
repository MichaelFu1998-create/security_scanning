def canonical_circulation(elements: T, key: Optional[Callable[[T], bool]] = None) -> T:
    """Get get a canonical representation of the ordered collection by finding its minimum circulation with the
    given sort key
    """
    return min(get_circulations(elements), key=key)