def compute(self, bottomUpInput, enableLearn, enableInference=None):
    """
    Handle one compute, possibly learning.

    .. note::  It is an error to have both ``enableLearn`` and 
               ``enableInference`` set to False

    .. note:: By default, we don't compute the inference output when learning 
              because it slows things down, but you can override this by passing 
              in True for ``enableInference``.

    :param bottomUpInput: The bottom-up input as numpy list, typically from a 
           spatial pooler.
    :param enableLearn: (bool) If true, perform learning
    :param enableInference: (bool) If None, default behavior is to disable the 
           inference output when ``enableLearn`` is on. If true, compute the 
           inference output. If false, do not compute the inference output.

    :returns: TODO: document

    """
    # As a speed optimization for now (until we need online learning), skip
    # computing the inference output while learning
    if enableInference is None:
      if enableLearn:
        enableInference = False
      else:
        enableInference = True

    assert (enableLearn or enableInference)

    # Get the list of columns that have bottom-up
    activeColumns = bottomUpInput.nonzero()[0]
    if enableLearn:
      self.lrnIterationIdx += 1
    self.iterationIdx +=  1

    if self.verbosity >= 3:
      print "\n==== PY Iteration: %d =====" % (self.iterationIdx)
      print "Active cols:", activeColumns

    # Update segment duty cycles if we are crossing a "tier"
    # We determine if it's time to update the segment duty cycles. Since the
    # duty cycle calculation is a moving average based on a tiered alpha, it is
    # important that we update all segments on each tier boundary
    if enableLearn:
      if self.lrnIterationIdx in Segment.dutyCycleTiers:
        for c, i in itertools.product(xrange(self.numberOfCols),
                                      xrange(self.cellsPerColumn)):
          for segment in self.cells[c][i]:
            segment.dutyCycle()

    # Update the average input density
    if self.avgInputDensity is None:
      self.avgInputDensity = len(activeColumns)
    else:
      self.avgInputDensity = (0.99 * self.avgInputDensity +
                              0.01 * len(activeColumns))

    # First, update the inference state
    # As a speed optimization for now (until we need online learning), skip
    # computing the inference output while learning
    if enableInference:
      self._updateInferenceState(activeColumns)

    # Next, update the learning state
    if enableLearn:
      self._updateLearningState(activeColumns)

      # Apply global decay, and remove synapses and/or segments.
      # Synapses are removed if their permanence value is <= 0.
      # Segments are removed when they don't have synapses anymore.
      # Removal of synapses can trigger removal of whole segments!
      # todo: isolate the synapse/segment retraction logic so that
      # it can be called in adaptSegments, in the case where we
      # do global decay only episodically.
      if self.globalDecay > 0.0 and ((self.lrnIterationIdx % self.maxAge) == 0):
        for c, i in itertools.product(xrange(self.numberOfCols),
                                      xrange(self.cellsPerColumn)):

          segsToDel = [] # collect and remove outside the loop
          for segment in self.cells[c][i]:
            age = self.lrnIterationIdx - segment.lastActiveIteration
            if age <= self.maxAge:
              continue

            synsToDel = [] # collect and remove outside the loop
            for synapse in segment.syns:

              synapse[2] = synapse[2] - self.globalDecay # decrease permanence

              if synapse[2] <= 0:
                synsToDel.append(synapse) # add to list to delete

            # 1 for sequenceSegment flag
            if len(synsToDel) == segment.getNumSynapses():
              segsToDel.append(segment) # will remove the whole segment
            elif len(synsToDel) > 0:
              for syn in synsToDel: # remove some synapses on segment
                segment.syns.remove(syn)

          for seg in segsToDel: # remove some segments of this cell
            self._cleanUpdatesList(c, i, seg)
            self.cells[c][i].remove(seg)

    # Update the prediction score stats
    # Learning always includes inference
    if self.collectStats:
      if enableInference:
        predictedState = self.infPredictedState['t-1']
      else:
        predictedState = self.lrnPredictedState['t-1']
      self._updateStatsInferEnd(self._internalStats,
                                activeColumns,
                                predictedState,
                                self.colConfidence['t-1'])

    # Finally return the TM output
    output = self._computeOutput()

    # Print diagnostic information based on the current verbosity level
    self.printComputeEnd(output, learn=enableLearn)

    self.resetCalled = False
    return output