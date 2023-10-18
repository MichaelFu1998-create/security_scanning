def center_data(data, vmin, vmax):
    """Clips data on [vmin, vmax]; then rescales to [0,1]"""
    ans = data - vmin
    ans /= (vmax - vmin)
    return np.clip(ans, 0, 1)