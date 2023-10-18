def map_chunk(func, array, out_array):
    """Map with `func`, chunk by chunk, the input pytable `array`.
    The result is stored in the output pytable array `out_array`.
    """
    for slice in iter_chunk_slice(array.shape[-1], array.chunkshape[-1]):
        out_array.append(func(array[..., slice]))
    return out_array