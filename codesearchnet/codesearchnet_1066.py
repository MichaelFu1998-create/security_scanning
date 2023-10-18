def setSeed(self, seed):
    """Set the random seed and the numpy seed
    Parameters:
    --------------------------------------------------------------------
    seed:             random seed
    """

    rand.seed(seed)
    np.random.seed(seed)