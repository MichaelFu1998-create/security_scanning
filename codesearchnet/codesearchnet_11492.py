def and_fault(a, b, out, fault):
    """Returns True if AND(a, b) == out and fault == 0 or AND(a, b) != out and fault == 1."""
    if (a and b) == out:
        return fault == 0
    else:
        return fault == 1