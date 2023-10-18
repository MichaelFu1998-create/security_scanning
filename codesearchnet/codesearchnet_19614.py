def snoise2d(size, z=0.0, scale=0.05, octaves=1, persistence=0.25, lacunarity=2.0):
    """
    z value as like a seed
    """
    import noise
    data = np.empty(size, dtype='float32')
    for y in range(size[0]):
        for x in range(size[1]):
            v = noise.snoise3(x * scale, y * scale, z,
                              octaves=octaves, persistence=persistence, lacunarity=lacunarity)
            data[x, y] = v
    data = data * 0.5 + 0.5
    if __debug__:
        assert data.min() >= 0. and data.max() <= 1.0
    return data