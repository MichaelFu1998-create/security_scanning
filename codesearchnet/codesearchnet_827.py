def getOutputNames(self):
    """
    Returns list of output names in spec.
    """
    outputs = self.getSpec().outputs
    return [outputs.getByIndex(i)[0] for i in xrange(outputs.getCount())]