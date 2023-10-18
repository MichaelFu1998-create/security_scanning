def assertNoTMDiffs(tms):
  """
  Check for diffs among the TM instances in the passed in tms dict and
  raise an assert if any are detected

  Parameters:
  ---------------------------------------------------------------------
  tms:                  dict of TM instances
  """

  if len(tms) == 1:
    return
  if len(tms) > 2:
    raise "Not implemented for more than 2 TMs"

  same = fdrutils.tmDiff2(tms.values(), verbosity=VERBOSITY)
  assert(same)
  return