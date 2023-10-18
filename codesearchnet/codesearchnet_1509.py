def advance(self):
    """ Advances the iteration;

    Returns:      True if more iterations remain; False if this is the final
                  iteration.
    """
    hasMore = True
    try:
      self.__iter.next()
    except StopIteration:
      self.__iter = None
      hasMore = False

    return hasMore