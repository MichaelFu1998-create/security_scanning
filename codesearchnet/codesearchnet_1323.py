def enableTap(self, tapPath):
    """
    Begin writing output tap files.

    :param tapPath: (string) base name of the output tap files to write.
    """

    self._tapFileIn = open(tapPath + '.in', 'w')
    self._tapFileOut = open(tapPath + '.out', 'w')