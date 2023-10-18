def random_product(iter1, iter2):
    """ 
    Random sampler for equal_splits functions
    """
    iter4 = np.concatenate([
        np.random.choice(iter1, 2, replace=False),
        np.random.choice(iter2, 2, replace=False)
        ])
    return iter4