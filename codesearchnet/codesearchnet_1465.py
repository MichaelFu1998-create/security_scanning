def reset(self):
    """
    Indicates the start of a new sequence. Clears any predictions and makes sure
    synapses don't grow to the currently active cells in the next time step.
    """
    self.activeCells = []
    self.winnerCells = []
    self.activeSegments = []
    self.matchingSegments = []