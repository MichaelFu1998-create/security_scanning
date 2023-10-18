def snoise2dvec(size, *params, **kwargs):  #, vlacunarity):
    """
    vector parameters
    :param size:
    :param vz:
    :param vscale:
    :param voctave:
    :param vpersistence:
    :param vlacunarity:
    :return:
    """
    data = (snoise2d(size, *p, **kwargs) for p in zip(*params))  # , vlacunarity))
    return np.stack(data, 0)