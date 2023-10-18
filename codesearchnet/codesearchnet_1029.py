def sameSegment(seg1, seg2):
  """Return True if seg1 and seg2 are identical, ignoring order of synapses"""
  result = True

  # check sequence segment, total activations etc. In case any are floats,
  # check that they are within 0.001.
  for field in [1, 2, 3, 4, 5, 6]:
    if abs(seg1[0][field] - seg2[0][field]) > 0.001:
      result = False

  # Compare number of synapses
  if len(seg1[1:]) != len(seg2[1:]):
    result = False

  # Now compare synapses, ignoring order of synapses
  for syn in seg2[1:]:
    if syn[2] <= 0:
      print "A synapse with zero permanence encountered"
      result = False
  if result == True:
    for syn in seg1[1:]:
      if syn[2] <= 0:
        print "A synapse with zero permanence encountered"
        result = False
      res = sameSynapse(syn, seg2[1:])
      if res == False:
        result = False

  return result