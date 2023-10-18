def expValue(self, pred):
    """ Helper function to return a scalar value representing the expected
        value of a probability distribution
    """
    if len(pred) == 1:
      return pred.keys()[0]

    return sum([x*p for x,p in pred.items()])