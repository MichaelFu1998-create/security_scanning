def split_rand(data_or_size, ratio, seed):
    """
    data(1-ratio), data(with ratio) = split_rand(data_or_size, ratio, seed)
    :param data_or_size: data or count
    :param ratio:
    :param seed:
    :return:
    """
    if not isinstance(data_or_size, int):
        sz = len(data_or_size)
        data = np.asarray(data_or_size)
    else:
        sz = data_or_size
        data = np.arange(sz)
    if not ratio:
        return data, []

    i = np.zeros(sz, dtype='bool')
    lattersz = int(sz * ratio)
    i[:lattersz] = True

    with np_seed(seed):
        np.random.shuffle(i)

    return data[~i], data[i]