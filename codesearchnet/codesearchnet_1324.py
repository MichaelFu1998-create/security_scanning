def disableTap(self):
    """
    Disable writing of output tap files.
    """

    if self._tapFileIn is not None:
      self._tapFileIn.close()
      self._tapFileIn = None
    if self._tapFileOut is not None:
      self._tapFileOut.close()
      self._tapFileOut = None