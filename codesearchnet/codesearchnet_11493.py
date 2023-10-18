def or_fault(a, b, out, fault):
    """Returns True if OR(a, b) == out and fault == 0 or OR(a, b) != out and fault == 1."""
    if (a or b) == out:
        return fault == 0
    else:
        return fault == 1