def compute(self, activeColumns, learn=True):
    """
    Perform one time step of the Temporal Memory algorithm.

    This method calls :meth:`activateCells`, then calls 
    :meth:`activateDendrites`. Using :class:`TemporalMemory` via its 
    :meth:`compute` method ensures that you'll always be able to call 
    :meth:`getPredictiveCells` to get predictions for the next time step.

    :param activeColumns: (iter) Indices of active columns.

    :param learn: (bool) Whether or not learning is enabled.
    """
    self.activateCells(sorted(activeColumns), learn)
    self.activateDendrites(learn)