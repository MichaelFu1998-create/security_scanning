def getInputNames(self):
    """
    Returns list of input names in spec.
    """
    inputs = self.getSpec().inputs
    return [inputs.getByIndex(i)[0] for i in xrange(inputs.getCount())]