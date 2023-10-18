def _getFuncPtrAndParams(self, funcName):
    """ Given the name of an aggregation function, returns the function pointer
    and param.

    Parameters:
    ------------------------------------------------------------------------
    funcName:  a string (name of function) or funcPtr
    retval:   (funcPtr, param)
    """

    params = None
    if isinstance(funcName, basestring):
      if funcName == 'sum':
        fp = _aggr_sum
      elif funcName == 'first':
        fp = _aggr_first
      elif funcName == 'last':
        fp = _aggr_last
      elif funcName == 'mean':
        fp = _aggr_mean
      elif funcName == 'max':
        fp = max
      elif funcName == 'min':
        fp = min
      elif funcName == 'mode':
        fp = _aggr_mode
      elif funcName.startswith('wmean:'):
        fp = _aggr_weighted_mean
        paramsName = funcName[6:]
        params = [f[0] for f in self._inputFields].index(paramsName)
    else:
      fp = funcName

    return (fp, params)