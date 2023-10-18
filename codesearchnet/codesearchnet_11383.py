def filter_savitzky_golay(y, window_size=5, order=2, deriv=0, rate=1):
    """Smooth (and optionally differentiate) with a Savitzky-Golay filter."""
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError:
        raise ValueError('window_size and order must be integers')

    if window_size % 2 != 1 or window_size < 1:
        raise ValueError('window_size size must be a positive odd number')
    if window_size < order + 2:
        raise ValueError('window_size is too small for the polynomials order')

    order_range = range(order + 1)
    half_window = (window_size - 1) // 2

    # precompute limits
    minimum = np.min(y)
    maximum = np.max(y)
    # precompute coefficients
    b = np.mat([
        [k ** i for i in order_range]
        for k in range(-half_window, half_window + 1)
    ])
    m = np.linalg.pinv(b).A[deriv] * rate ** deriv * math.factorial(deriv)
    # pad the signal at the extremes with values taken from the original signal
    firstvals = y[0] - np.abs(y[1:half_window+1][::-1] - y[0])
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.clip(
        np.convolve(m[::-1], y, mode='valid'),
        minimum,
        maximum,
    )