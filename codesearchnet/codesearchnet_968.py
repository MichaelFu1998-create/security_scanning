def _isInt(x, precision = 0.0001):
  """
  Return (isInt, intValue) for a given floating point number.

  Parameters:
  ----------------------------------------------------------------------
  x:  floating point number to evaluate
  precision: desired precision
  retval:   (isInt, intValue)
            isInt: True if x is close enough to an integer value
            intValue: x as an integer
  """

  xInt = int(round(x))
  return (abs(x - xInt) < precision * x, xInt)