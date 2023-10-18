def _getStartRow(self, bookmark):
    """ Extracts start row from the bookmark information
    """
    bookMarkDict = json.loads(bookmark)

    realpath = os.path.realpath(self._filename)

    bookMarkFile = bookMarkDict.get('filepath', None)

    if bookMarkFile != realpath:
      print ("Ignoring bookmark due to mismatch between File's "
             "filename realpath vs. bookmark; realpath: %r; bookmark: %r") % (
        realpath, bookMarkDict)
      return 0
    else:
      return bookMarkDict['currentRow']