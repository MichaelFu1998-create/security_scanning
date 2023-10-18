def initialize(self):
    """
    Overrides :meth:`nupic.bindings.regions.PyRegion.PyRegion.initialize`.

    Is called once by NuPIC before the first call to compute().
    Initializes self._sdrClassifier if it is not already initialized.
    """
    if self._sdrClassifier is None:
      self._sdrClassifier = SDRClassifierFactory.create(
        steps=self.stepsList,
        alpha=self.alpha,
        verbosity=self.verbosity,
        implementation=self.implementation,
      )