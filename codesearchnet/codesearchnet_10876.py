def iter_chunksize(num_samples, chunksize):
    """Iterator used to iterate in chunks over an array of size `num_samples`.
    At each iteration returns `chunksize` except for the last iteration.
    """
    last_chunksize = int(np.mod(num_samples, chunksize))
    chunksize = int(chunksize)
    for _ in range(int(num_samples) // chunksize):
        yield chunksize
    if last_chunksize > 0:
        yield last_chunksize