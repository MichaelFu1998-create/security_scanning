def iter_chunk_index(num_samples, chunksize):
    """Iterator used to iterate in chunks over an array of size `num_samples`.

    At each iteration returns a start and stop index for a slice of size
    `chunksize`. In the last iteration the slice may be smaller.
    """
    i = 0
    for c_size in iter_chunksize(num_samples, chunksize):
        yield i, i + c_size
        i += c_size