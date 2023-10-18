def handleLogOutput(self, output):
    """
    Write outputs to output tap file.

    :param outputs: (iter) some outputs.
    """
    #raise Exception('MULTI-LINE DUMMY\nMULTI-LINE DUMMY')
    if self._tapFileOut is not None:
      for k in range(len(output)):
        print >> self._tapFileOut, output[k],
      print >> self._tapFileOut