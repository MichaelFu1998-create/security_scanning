def updateRow(self, row, distribution):
    """
    Add distribution to row row.
    Distribution should be an array of probabilities or counts.

    :param row:   Integer index of the row to add to.
                  May be larger than the current number of rows, in which case
                  the histogram grows.
    :param distribution: Array of length equal to the number of columns.
    """
    self.grow(row+1, len(distribution))
    self.hist_.axby(row, 1, 1, distribution)
    self.rowSums_[row] += distribution.sum()
    self.colSums_ += distribution
    self.hack_ = None