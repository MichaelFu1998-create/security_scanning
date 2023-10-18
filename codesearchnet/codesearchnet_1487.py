def AreaUnderCurve(x, y):
    """Compute Area Under the Curve (AUC) using the trapezoidal rule

    Parameters
    ----------
    x : array, shape = [n]
        x coordinates

    y : array, shape = [n]
        y coordinates

    Returns
    -------
    auc : float

    Examples
    --------
    >>> import numpy as np
    >>> from sklearn import metrics
    >>> y = np.array([1, 1, 2, 2])
    >>> pred = np.array([0.1, 0.4, 0.35, 0.8])
    >>> fpr, tpr, thresholds = metrics.roc_curve(y, pred)
    >>> metrics.auc(fpr, tpr)
    0.75

    """
    #x, y = check_arrays(x, y)
    if x.shape[0] != y.shape[0]:
        raise ValueError('x and y should have the same shape'
                         ' to compute area under curve,'
                         ' but x.shape = %s and y.shape = %s.'
                         % (x.shape, y.shape))
    if x.shape[0] < 2:
        raise ValueError('At least 2 points are needed to compute'
                         ' area under curve, but x.shape = %s' % x.shape)

    # reorder the data points according to the x axis
    order = np.argsort(x)
    x = x[order]
    y = y[order]

    h = np.diff(x)
    area = np.sum(h * (y[1:] + y[:-1])) / 2.0
    return area