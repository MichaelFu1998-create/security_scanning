def main():
  """Run according to options in sys.argv and diff classifiers."""
  initLogging(verbose=True)

  # Initialize PRNGs
  initExperimentPrng()

  # Mock out the creation of the SDRClassifier.
  @staticmethod
  def _mockCreate(*args, **kwargs):
    kwargs.pop('implementation', None)
    return SDRClassifierDiff(*args, **kwargs)
  SDRClassifierFactory.create = _mockCreate

  # Run it!
  runExperiment(sys.argv[1:])