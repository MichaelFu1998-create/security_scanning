def get_cutoff(value: float, cutoff: Optional[float] = None) -> int:
    """Assign if a value is greater than or less than a cutoff."""
    cutoff = cutoff if cutoff is not None else 0

    if value > cutoff:
        return 1

    if value < (-1 * cutoff):
        return - 1

    return 0