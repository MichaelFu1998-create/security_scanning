def round_to_nearest(x):
  """Python 3 style round:  round a float x to the nearest int, but
  unlike the builtin Python 2.x round function:

    - return an int, not a float
    - do round-half-to-even, not round-half-away-from-zero.

  We assume that x is finite and nonnegative; except wrong results
  if you use this for negative x.

  """
  int_part = int(x)
  frac_part = x - int_part
  if frac_part > 0.5 or frac_part == 0.5 and int_part & 1 == 1:
    int_part += 1
  return int_part