def getBookmark(self):
    """
    Gets a bookmark or anchor to the current position.

    :returns: an anchor to the current position in the data. Passing this
              anchor to a constructor makes the current position to be the first
              returned record.
    """

    if self._write and self._recordCount==0:
      return None

    rowDict = dict(filepath=os.path.realpath(self._filename),
                   currentRow=self._recordCount)
    return json.dumps(rowDict)