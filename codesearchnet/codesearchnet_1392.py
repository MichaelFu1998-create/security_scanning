def removeIds(self, idsToRemove):
    """
    There are two caveats. First, this is a potentially slow operation. Second,
    pattern indices will shift if patterns before them are removed.

    :param idsToRemove: A list of row indices to remove.
    """
    # Form a list of all categories to remove
    rowsToRemove = [k for k, rowID in enumerate(self._categoryRecencyList) \
                    if rowID in idsToRemove]

    # Remove rows from the classifier
    self._removeRows(rowsToRemove)