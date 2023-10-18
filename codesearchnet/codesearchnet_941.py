def _getTPClass(temporalImp):
  """ Return the class corresponding to the given temporalImp string
  """

  if temporalImp == 'py':
    return backtracking_tm.BacktrackingTM
  elif temporalImp == 'cpp':
    return backtracking_tm_cpp.BacktrackingTMCPP
  elif temporalImp == 'tm_py':
    return backtracking_tm_shim.TMShim
  elif temporalImp == 'tm_cpp':
    return backtracking_tm_shim.TMCPPShim
  elif temporalImp == 'monitored_tm_py':
    return backtracking_tm_shim.MonitoredTMShim
  else:
    raise RuntimeError("Invalid temporalImp '%s'. Legal values are: 'py', "
              "'cpp', 'tm_py', 'monitored_tm_py'" % (temporalImp))