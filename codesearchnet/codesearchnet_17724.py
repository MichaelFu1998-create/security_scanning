def _strBinary(n):
    """Conert an integer to binary (i.e., a string of 1s and 0s)."""
    results = []
    for i in range(8):
        n, r = divmod(n, 2)
        results.append('01'[r])
    results.reverse()
    return ''.join(results)