def evalSequences(tms,
                  trainingSequences,
                  testSequences = None,
                  nTrainRepetitions = 1,
                  doResets = True,
                  **kwargs):

  """Train the TMs on the entire training set for nTrainRepetitions in a row.
  Then run the test set through inference once and return the inference stats.

  Parameters:
  ---------------------------------------------------------------------
  tms:                  dict of TM instances
  trainingSequences:    list of training sequences. Each sequence is a list
                        of TM input patterns
  testSequences:        list of test sequences. If None, we will test against
                        the trainingSequences
  nTrainRepetitions:    Number of times to run the training set through the TM
  doResets:             If true, send a reset to the TM between each sequence
  """

  # If no test sequence is specified, use the first training sequence
  if testSequences == None:
    testSequences = trainingSequences

  # First TM instance is used by default for verbose printing of input values,
  #  etc.
  firstTM = tms.values()[0]

  assertNoTMDiffs(tms)

  # =====================================================================
  # Loop through the training set nTrainRepetitions times
  # ==========================================================================
  for trainingNum in xrange(nTrainRepetitions):
    if VERBOSITY >= 2:
      print "\n##############################################################"
      print "################# Training round #%d of %d #################" \
                % (trainingNum, nTrainRepetitions)
      for (name,tm) in tms.iteritems():
        print "TM parameters for %s: " % (name)
        print "---------------------"
        tm.printParameters()
        print

    # ======================================================================
    # Loop through the sequences in the training set
    numSequences = len(testSequences)
    for sequenceNum, trainingSequence in enumerate(trainingSequences):
      numTimeSteps = len(trainingSequence)

      if VERBOSITY >= 2:
        print "\n================= Sequence #%d of %d ================" \
                  % (sequenceNum, numSequences)

      if doResets:
        for tm in tms.itervalues():
          tm.reset()

      # --------------------------------------------------------------------
      # Train each element of the sequence
      for t, x in enumerate(trainingSequence):

        # Print Verbose info about this element
        if VERBOSITY >= 2:
          print
          if VERBOSITY >= 3:
            print "------------------------------------------------------------"
          print "--------- sequence: #%d of %d, timeStep: #%d of %d -----------" \
                  % (sequenceNum, numSequences, t, numTimeSteps)
          firstTM.printInput(x)
          print "input nzs:", x.nonzero()

        # Train in this element
        x = numpy.array(x).astype('float32')
        for tm in tms.itervalues():
          tm.learn(x, enableInference=True)

        # Print the input and output states
        if VERBOSITY >= 3:
          for (name,tm) in tms.iteritems():
            print "I/O states of %s TM:" % (name)
            print "-------------------------------------",
            tm.printStates(printPrevious = (VERBOSITY >= 5))
            print

        assertNoTMDiffs(tms)

        # Print out number of columns that weren't predicted
        if VERBOSITY >= 2:
          for (name,tm) in tms.iteritems():
            stats = tm.getStats()
            print "# of unpredicted columns for %s TM: %d of %d" \
                % (name, stats['curMissing'], x.sum())
            numBurstingCols = tm.infActiveState['t'].min(axis=1).sum()
            print "# of bursting columns for %s TM: %d of %d" \
                % (name, numBurstingCols, x.sum())


      # Print the trained cells
      if VERBOSITY >= 4:
        print "Sequence %d finished." % (sequenceNum)
        for (name,tm) in tms.iteritems():
          print "All cells of %s TM:" % (name)
          print "-------------------------------------",
          tm.printCells()
          print

    # --------------------------------------------------------------------
    # Done training all sequences in this round, print the total number of
    #  missing, extra columns and make sure it's the same among the TMs
    if VERBOSITY >= 2:
      print
    prevResult = None
    for (name,tm) in tms.iteritems():
      stats = tm.getStats()
      if VERBOSITY >= 1:
        print "Stats for %s TM over all sequences for training round #%d of %d:" \
                % (name, trainingNum, nTrainRepetitions)
        print "   total missing:", stats['totalMissing']
        print "   total extra:", stats['totalExtra']

      if prevResult is None:
        prevResult = (stats['totalMissing'], stats['totalExtra'])
      else:
        assert (stats['totalMissing'] == prevResult[0])
        assert (stats['totalExtra'] == prevResult[1])

      tm.resetStats()


  # =====================================================================
  # Finish up learning
  if VERBOSITY >= 3:
    print "Calling trim segments"
  prevResult = None
  for tm in tms.itervalues():
    nSegsRemoved, nSynsRemoved = tm.trimSegments()
    if prevResult is None:
      prevResult = (nSegsRemoved, nSynsRemoved)
    else:
      assert (nSegsRemoved == prevResult[0])
      assert (nSynsRemoved == prevResult[1])

  assertNoTMDiffs(tms)

  if VERBOSITY >= 4:
    print "Training completed. Complete state:"
    for (name,tm) in tms.iteritems():
      print "%s:" % (name)
      tm.printCells()
      print


  # ==========================================================================
  # Infer
  # ==========================================================================
  if VERBOSITY >= 2:
    print "\n##############################################################"
    print "########################## Inference #########################"

  # Reset stats in all TMs
  for tm in tms.itervalues():
    tm.resetStats()

  # -------------------------------------------------------------------
  # Loop through the test sequences
  numSequences = len(testSequences)
  for sequenceNum, testSequence in enumerate(testSequences):
    numTimeSteps = len(testSequence)

    # Identify this sequence
    if VERBOSITY >= 2:
      print "\n================= Sequence %d of %d ================" \
                % (sequenceNum, numSequences)

    # Send in the rest
    if doResets:
      for tm in tms.itervalues():
        tm.reset()

    # -------------------------------------------------------------------
    # Loop through the elements of this sequence
    for t,x in enumerate(testSequence):

      # Print verbose info about this element
      if VERBOSITY >= 2:
        print
        if VERBOSITY >= 3:
          print "------------------------------------------------------------"
        print "--------- sequence: #%d of %d, timeStep: #%d of %d -----------" \
                % (sequenceNum, numSequences, t, numTimeSteps)
        firstTM.printInput(x)
        print "input nzs:", x.nonzero()

      # Infer on this element
      for tm in tms.itervalues():
        tm.infer(x)

      assertNoTMDiffs(tms)

      # Print out number of columns that weren't predicted
      if VERBOSITY >= 2:
        for (name,tm) in tms.iteritems():
          stats = tm.getStats()
          print "# of unpredicted columns for %s TM: %d of %d" \
              % (name, stats['curMissing'], x.sum())

      # Debug print of internal state
      if VERBOSITY >= 3:
        for (name,tm) in tms.iteritems():
          print "I/O states of %s TM:" % (name)
          print "-------------------------------------",
          tm.printStates(printPrevious = (VERBOSITY >= 5),
                         printLearnState = False)
          print

    # Done with this sequence
    # Debug print of all stats of the TMs
    if VERBOSITY >= 4:
      print
      for (name,tm) in tms.iteritems():
        print "Interim internal stats for %s TM:" % (name)
        print "---------------------------------"
        pprint.pprint(tm.getStats())
        print


  if VERBOSITY >= 2:
    print "\n##############################################################"
    print "####################### Inference Done #######################"

  # Get the overall stats for each TM and return them
  tmStats = dict()
  for (name,tm) in tms.iteritems():
    tmStats[name] = stats = tm.getStats()
    if VERBOSITY >= 2:
      print "Stats for %s TM over all sequences:" % (name)
      print "   total missing:", stats['totalMissing']
      print "   total extra:", stats['totalExtra']

  for (name,tm) in tms.iteritems():
    if VERBOSITY >= 3:
      print "\nAll internal stats for %s TM:" % (name)
      print "-------------------------------------",
      pprint.pprint(tmStats[name])
      print

  return tmStats