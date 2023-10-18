def printSegmentUpdates(self):
    """
    Overrides :meth:`nupic.algorithms.backtracking_tm.BacktrackingTM.printSegmentUpdates`.
    """
    # TODO: need to add C++ accessors to implement this method
    assert False
    print "=== SEGMENT UPDATES ===, Num = ", len(self.segmentUpdates)
    for key, updateList in self.segmentUpdates.iteritems():
      c,i = key[0],key[1]
      print c,i,updateList