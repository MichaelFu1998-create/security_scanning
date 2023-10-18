def float_pack(x, size):
  """Convert a Python float x into a 64-bit unsigned integer
  with the same byte representation."""

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

  sign = math.copysign(1.0, x) < 0.0
  if math.isinf(x):
    mant = 0
    exp = MAX_EXP - MIN_EXP + 2
  elif math.isnan(x):
    mant = 1 << (MANT_DIG - 2)  # other values possible
    exp = MAX_EXP - MIN_EXP + 2
  elif x == 0.0:
    mant = 0
    exp = 0
  else:
    m, e = math.frexp(abs(x))  # abs(x) == m * 2**e
    exp = e - (MIN_EXP - 1)
    if exp > 0:
      # Normal case.
      mant = round_to_nearest(m * (1 << MANT_DIG))
      mant -= 1 << MANT_DIG - 1
    else:
      # Subnormal case.
      if exp + MANT_DIG - 1 >= 0:
        mant = round_to_nearest(m * (1 << exp + MANT_DIG - 1))
      else:
        mant = 0
      exp = 0

    # Special case: rounding produced a MANT_DIG-bit mantissa.
    assert 0 <= mant <= 1 << MANT_DIG - 1
    if mant == 1 << MANT_DIG - 1:
      mant = 0
      exp += 1

    # Raise on overflow (in some circumstances, may want to return
    # infinity instead).
    if exp >= MAX_EXP - MIN_EXP + 2:
      raise OverflowError("float too large to pack in this format")

  # check constraints
  assert 0 <= mant < 1 << MANT_DIG - 1
  assert 0 <= exp <= MAX_EXP - MIN_EXP + 2
  assert 0 <= sign <= 1
  return ((sign << BITS - 1) | (exp << MANT_DIG - 1)) | mant