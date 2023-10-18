def initialize(self):
    """
    Overrides :meth:`~nupic.bindings.regions.PyRegion.initialize`.
    """
    # Allocate appropriate temporal memory object
    # Retrieve the necessary extra arguments that were handled automatically
    autoArgs = dict((name, getattr(self, name))
                    for name in self._temporalArgNames)

    if self._tfdr is None:
      tpClass = _getTPClass(self.temporalImp)

      if self.temporalImp in ['py', 'cpp', 'r',
                              'tm_py', 'tm_cpp',
                              'monitored_tm_py',]:
        self._tfdr = tpClass(
             numberOfCols=self.columnCount,
             cellsPerColumn=self.cellsPerColumn,
             **autoArgs)
      else:
        raise RuntimeError("Invalid temporalImp")