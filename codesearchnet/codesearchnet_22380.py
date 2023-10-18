def get_indices_list(s: Any) -> List[str]:
    """ Retrieve a list of characters and escape codes where each escape
        code uses only one index. The indexes will not match up with the
        indexes in the original string.
    """
    indices = get_indices(s)
    return [
        indices[i] for i in sorted(indices, key=int)
    ]