def _seed(self, seed=-1):
    """
    Initialize the random seed
    """
    if seed != -1:
      self.random = NupicRandom(seed)
    else:
      self.random = NupicRandom()