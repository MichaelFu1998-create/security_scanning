def xor_fault(a, b, out, fault):
    """Returns True if XOR(a, b) == out and fault == 0 or XOR(a, b) != out and fault == 1."""
    if (a != b) == out:
        return fault == 0
    else:
        return fault == 1