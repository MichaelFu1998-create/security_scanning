def iso_reference_str2int(n):
    """Creates the huge number from ISO alphanumeric ISO reference"""
    n = n.upper()
    numbers = []
    for c in n:
        iso_reference_valid_char(c)
        if c in ISO_REFERENCE_VALID_NUMERIC:
            numbers.append(c)
        else:
            numbers.append(str(iso_reference_char2int(c)))
    return int(''.join(numbers))