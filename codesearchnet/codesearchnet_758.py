def enableConcurrencyChecks(maxConcurrency, raiseException=True):
  """ Enable the diagnostic feature for debugging unexpected concurrency in
  acquiring ConnectionWrapper instances.

  NOTE: This MUST be done early in your application's execution, BEFORE any
  accesses to ConnectionFactory or connection policies from your application
  (including imports and sub-imports of your app).

  Parameters:
  ----------------------------------------------------------------
  maxConcurrency:   A non-negative integer that represents the maximum expected
                      number of outstanding connections.  When this value is
                      exceeded, useful information will be logged and, depending
                      on the value of the raiseException arg,
                      ConcurrencyExceededError may be raised.
  raiseException:   If true, ConcurrencyExceededError will be raised when
                      maxConcurrency is exceeded.
  """
  global g_max_concurrency, g_max_concurrency_raise_exception

  assert maxConcurrency >= 0

  g_max_concurrency = maxConcurrency
  g_max_concurrency_raise_exception = raiseException
  return