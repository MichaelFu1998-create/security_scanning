def weighted_mean_and_std(values, weights):
    """
    Returns the weighted average and standard deviation.

    values, weights -- numpy ndarrays with the same shape.
    """
    average = np.average(values, weights=weights, axis=0)
    variance = np.dot(weights, (values - average) ** 2) / weights.sum()  # Fast and numerically precise
    return (average, np.sqrt(variance))