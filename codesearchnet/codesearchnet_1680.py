def _updateAvgLearnedSeqLength(self, prevSeqLength):
    """Update our moving average of learned sequence length."""
    if self.lrnIterationIdx < 100:
      alpha = 0.5
    else:
      alpha = 0.1

    self.avgLearnedSeqLength = ((1.0 - alpha) * self.avgLearnedSeqLength +
                                (alpha * prevSeqLength))