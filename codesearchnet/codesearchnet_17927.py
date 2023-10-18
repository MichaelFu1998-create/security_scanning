def harris_feature(im, region_size=5, to_return='harris', scale=0.05):
    """
    Harris-motivated feature detection on a d-dimensional image.

    Parameters
    ---------
        im
        region_size
        to_return : {'harris','matrix','trace-determinant'}

    """
    ndim = im.ndim
    #1. Gradient of image
    grads = [nd.sobel(im, axis=i) for i in range(ndim)]
    #2. Corner response matrix
    matrix = np.zeros((ndim, ndim) + im.shape)
    for a in range(ndim):
        for b in range(ndim):
            matrix[a,b] = nd.filters.gaussian_filter(grads[a]*grads[b],
                    region_size)
    if to_return == 'matrix':
        return matrix
    #3. Trace, determinant
    trc = np.trace(matrix, axis1=0, axis2=1)
    det = np.linalg.det(matrix.T).T
    if to_return == 'trace-determinant':
        return trc, det
    else:
        #4. Harris detector:
        harris = det - scale*trc*trc
        return harris