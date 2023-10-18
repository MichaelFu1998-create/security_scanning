def reduce_chunk(func, array):
    """Reduce with `func`, chunk by chunk, the passed pytable `array`.
    """
    res = []
    for slice in iter_chunk_slice(array.shape[-1], array.chunkshape[-1]):
        res.append(func(array[..., slice]))
    return func(res)