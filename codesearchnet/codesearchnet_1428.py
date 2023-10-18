def seekFromEnd(self, numRecords):
    """
    Seeks to ``numRecords`` from the end and returns a bookmark to the new
    position.

    :param numRecords: how far to seek from end of file.
    :return: bookmark to desired location.
    """
    self._file.seek(self._getTotalLineCount() - numRecords)
    return self.getBookmark()