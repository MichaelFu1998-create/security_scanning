def sameSynapse(syn, synapses):
  """Given a synapse and a list of synapses, check whether this synapse
  exist in the list.  A synapse is represented as [col, cell, permanence].
  A synapse matches if col and cell are identical and the permanence value is
  within 0.001."""
  for s in synapses:
    if (s[0]==syn[0]) and (s[1]==syn[1]) and (abs(s[2]-syn[2]) <= 0.001):
      return True
  return False