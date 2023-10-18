def _adaptSegment(self, segUpdate):
    """
    This function applies segment update information to a segment in a
    cell.

    Synapses on the active list get their permanence counts incremented by
    permanenceInc. All other synapses get their permanence counts decremented
    by permanenceDec.

    We also increment the positiveActivations count of the segment.

    :param segUpdate SegmentUpdate instance
    :returns: True if some synapses were decremented to 0 and the segment is a
             candidate for trimming
    """
    # This will be set to True if detect that any syapses were decremented to
    #  0
    trimSegment = False

    # segUpdate.segment is None when creating a new segment
    c, i, segment = segUpdate.columnIdx, segUpdate.cellIdx, segUpdate.segment

    # update.activeSynapses can be empty.
    # If not, it can contain either or both integers and tuples.
    # The integers are indices of synapses to update.
    # The tuples represent new synapses to create (src col, src cell in col).
    # We pre-process to separate these various element types.
    # synToCreate is not empty only if positiveReinforcement is True.
    # NOTE: the synapse indices start at *1* to skip the segment flags.
    activeSynapses = segUpdate.activeSynapses
    synToUpdate = set([syn for syn in activeSynapses if type(syn) == int])

    # Modify an existing segment
    if segment is not None:

      if self.verbosity >= 4:
        print "Reinforcing segment #%d for cell[%d,%d]" % (segment.segID, c, i)
        print "  before:",
        segment.debugPrint()

      # Mark it as recently useful
      segment.lastActiveIteration = self.lrnIterationIdx

      # Update frequency and positiveActivations
      segment.positiveActivations += 1       # positiveActivations += 1
      segment.dutyCycle(active=True)

      # First, decrement synapses that are not active
      # s is a synapse *index*, with index 0 in the segment being the tuple
      # (segId, sequence segment flag). See below, creation of segments.
      lastSynIndex = len(segment.syns) - 1
      inactiveSynIndices = [s for s in xrange(0, lastSynIndex+1) \
                            if s not in synToUpdate]
      trimSegment = segment.updateSynapses(inactiveSynIndices,
                                           -self.permanenceDec)

      # Now, increment active synapses
      activeSynIndices = [syn for syn in synToUpdate if syn <= lastSynIndex]
      segment.updateSynapses(activeSynIndices, self.permanenceInc)

      # Finally, create new synapses if needed
      # syn is now a tuple (src col, src cell)
      synsToAdd = [syn for syn in activeSynapses if type(syn) != int]
      # If we have fixed resources, get rid of some old syns if necessary
      if self.maxSynapsesPerSegment > 0 \
          and len(synsToAdd) + len(segment.syns) > self.maxSynapsesPerSegment:
        numToFree = (len(segment.syns) + len(synsToAdd) -
                     self.maxSynapsesPerSegment)
        segment.freeNSynapses(numToFree, inactiveSynIndices, self.verbosity)
      for newSyn in synsToAdd:
        segment.addSynapse(newSyn[0], newSyn[1], self.initialPerm)

      if self.verbosity >= 4:
        print "   after:",
        segment.debugPrint()

    # Create a new segment
    else:

      # (segID, sequenceSegment flag, frequency, positiveActivations,
      #          totalActivations, lastActiveIteration)
      newSegment = Segment(tm=self, isSequenceSeg=segUpdate.sequenceSegment)

      # numpy.float32 important so that we can match with C++
      for synapse in activeSynapses:
        newSegment.addSynapse(synapse[0], synapse[1], self.initialPerm)

      if self.verbosity >= 3:
        print "New segment #%d for cell[%d,%d]" % (self.segID-1, c, i),
        newSegment.debugPrint()

      self.cells[c][i].append(newSegment)

    return trimSegment