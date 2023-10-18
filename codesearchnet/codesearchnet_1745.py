def float_unpack(Q, size, le):
  """Convert a 32-bit or 64-bit integer created
  by float_pack into a Python float."""

  if size == 8:
    MIN_EXP = -1021  # = sys.float_info.min_exp
    MAX_EXP = 1024   # = sys.float_info.max_exp
    MANT_DIG = 53    # = sys.float_info.mant_dig
    BITS = 64
  elif size == 4:
    MIN_EXP = -125   # C's FLT_MIN_EXP
    MAX_EXP = 128    # FLT_MAX_EXP
    MANT_DIG = 24    # FLT_MANT_DIG
    BITS = 32
  else:
    raise ValueError("invalid size value")

  if Q >> BITS:
    raise ValueError("input out of range")

  # extract pieces
  sign = Q >> BITS - 1
  exp = (Q & ((1 << BITS - 1) - (1 << MANT_DIG - 1))) >> MANT_DIG - 1
  mant = Q & ((1 << MANT_DIG - 1) - 1)

  if exp == MAX_EXP - MIN_EXP + 2:
    # nan or infinity
    result = float('nan') if mant else float('inf')
  elif exp == 0:
    # subnormal or zero
    result = math.ldexp(float(mant), MIN_EXP - MANT_DIG)
  else:
    # normal
    mant += 1 << MANT_DIG - 1
    result = math.ldexp(float(mant), exp + MIN_EXP - MANT_DIG - 1)
  return -result if sign else result