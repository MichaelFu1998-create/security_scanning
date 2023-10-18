def pick_coda_from_decimal(decimal):
    """Picks only a coda from a decimal."""
    decimal = Decimal(decimal)
    __, digits, exp = decimal.as_tuple()
    if exp < 0:
        return DIGIT_CODAS[digits[-1]]
    __, digits, exp = decimal.normalize().as_tuple()
    index = bisect_right(EXP_INDICES, exp) - 1
    if index < 0:
        return DIGIT_CODAS[digits[-1]]
    else:
        return EXP_CODAS[EXP_INDICES[index]]