def handleLogInput(self, inputs):
    """
    Write inputs to output tap file.
    
    :param inputs: (iter) some inputs.
    """

    if self._tapFileIn is not None:
      for input in inputs:
        for k in range(len(input)):
          print >> self._tapFileIn, input[k],
        print >> self._tapFileIn