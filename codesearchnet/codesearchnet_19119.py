def linear(Ks, dim, num_q, rhos, nus):
    r'''
    Estimates the linear inner product \int p q between two distributions,
    based on kNN distances.
    '''
    return _get_linear(Ks, dim)(num_q, rhos, nus)