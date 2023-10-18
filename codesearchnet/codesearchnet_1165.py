def infer(self, patternNZ, actValueList):
    """
    Return the inference value from one input sample. The actual
    learning happens in compute().

    :param patternNZ: list of the active indices from the output below
    :param classification: dict of the classification information:
                    bucketIdx: index of the encoder bucket
                    actValue:  actual value going into the encoder

    :return:    dict containing inference results, one entry for each step in
                self.steps. The key is the number of steps, the value is an
                array containing the relative likelihood for each bucketIdx
                starting from bucketIdx 0.

                for example:

                .. code-block:: python

                   {'actualValues': [0.0, 1.0, 2.0, 3.0]
                     1 : [0.1, 0.3, 0.2, 0.7]
                     4 : [0.2, 0.4, 0.3, 0.5]}
    """

    # Return value dict. For buckets which we don't have an actual value
    # for yet, just plug in any valid actual value. It doesn't matter what
    # we use because that bucket won't have non-zero likelihood anyways.

    # NOTE: If doing 0-step prediction, we shouldn't use any knowledge
    #  of the classification input during inference.
    if self.steps[0] == 0 or actValueList is None:
      defaultValue = 0
    else:
      defaultValue = actValueList[0]
    actValues = [x if x is not None else defaultValue
                 for x in self._actualValues]
    retval = {"actualValues": actValues}

    for nSteps in self.steps:
      predictDist = self.inferSingleStep(patternNZ, self._weightMatrix[nSteps])

      retval[nSteps] = predictDist

    return retval