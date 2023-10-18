def kfolds(n, k, sz, p_testset=None, seed=7238):
    """
    return train, valid  [,test]
    testset if p_testset
    :param n:
    :param k:
    :param sz:
    :param p_testset:
    :param seed:
    :return:
    """
    trains, tests = split_rand(sz, p_testset, seed)

    ntrain = len(trains)

    # np.random.seed(seed)
    with np_seed(seed):
        np.random.shuffle(trains)
    if n == k:
        # no split
        train, valid = trains, trains
    else:
        foldsz = ntrain // k

        itrain = np.arange(ntrain) // foldsz != n
        train = trains[itrain]
        valid = trains[~itrain]

    if not p_testset:
        return train, valid
    else:
        return train, valid, tests