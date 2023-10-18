def update(self, modelResult):
    """ Queue up the T(i+1) prediction value and emit a T(i)
    input/prediction pair, if possible.  E.g., if the previous T(i-1)
    iteration was learn-only, then we would not have a T(i) prediction in our
    FIFO and would not be able to emit a meaningful input/prediction
    pair.

    modelResult:    An opf_utils.ModelResult object that contains the model input
                    and output for the current timestep.
    """
    self.__writer.append(self.__inferenceShifter.shift(modelResult))