def _setup_index(index):
    """Shifts indicies as needed to account for one based indexing

    Positive indicies need to be reduced by one to match with zero based
    indexing.

    Zero is not a valid input, and as such will throw a value error.

    Arguments:
        index -     index to shift
    """
    index = int(index)
    if index > 0:
        index -= 1
    elif index == 0:
        # Zero indicies should not be allowed by default.
        raise ValueError
    return index