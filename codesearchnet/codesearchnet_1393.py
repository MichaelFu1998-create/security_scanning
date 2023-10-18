def removeCategory(self, categoryToRemove):
    """
    There are two caveats. First, this is a potentially slow operation. Second,
    pattern indices will shift if patterns before them are removed.

    :param categoryToRemove: Category label to remove
    """
    removedRows = 0
    if self._Memory is None:
      return removedRows

    # The internal category indices are stored in float
    # format, so we should compare with a float
    catToRemove = float(categoryToRemove)

    # Form a list of all categories to remove
    rowsToRemove = [k for k, catID in enumerate(self._categoryList) \
                    if catID == catToRemove]

    # Remove rows from the classifier
    self._removeRows(rowsToRemove)

    assert catToRemove not in self._categoryList