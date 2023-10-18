def _rindex(mylist: Sequence[T], x: T) -> int:
    """Index of the last occurrence of x in the sequence."""
    return len(mylist) - mylist[::-1].index(x) - 1