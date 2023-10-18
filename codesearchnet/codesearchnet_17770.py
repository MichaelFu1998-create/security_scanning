def orthonormal_complement_basis(v:NDim(1)):
    '''
    Return orthonormal basis of complement of vector.
    
    :param v: 1-dimensional numpy array 
    :return: Matrix whose .dot() computes coefficients w.r.t. an orthonormal basis of the complement of v 
        (i.e. whose row vectors form an orthonormal basis of the complement of v)
    '''
    _, _, V = np.linalg.svd(np.array([v]))
    return V[1:]