def remove_falsy_values(counter: Mapping[Any, int]) -> Mapping[Any, int]:
    """Remove all values that are zero."""
    return {
        label: count
        for label, count in counter.items()
        if count
    }