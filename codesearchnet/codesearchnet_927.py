def _allocateSpatialFDR(self, rfInput):
    """Allocate the spatial pooler instance."""
    if self._sfdr:
      return

    # Retrieve the necessary extra arguments that were handled automatically
    autoArgs = dict((name, getattr(self, name))
                     for name in self._spatialArgNames)

    # Instantiate the spatial pooler class.
    if ( (self.SpatialClass == CPPSpatialPooler) or
         (self.SpatialClass == PYSpatialPooler) ):

      autoArgs['columnDimensions'] = [self.columnCount]
      autoArgs['inputDimensions'] = [self.inputWidth]
      autoArgs['potentialRadius'] = self.inputWidth

      self._sfdr = self.SpatialClass(
        **autoArgs
      )