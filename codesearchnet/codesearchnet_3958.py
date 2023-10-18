def bin_variable(var, bins='fd'):  # bin with normalization
    """Bin variables w/ normalization."""
    var = np.array(var).astype(np.float)
    var = (var - np.mean(var)) / np.std(var)
    var = np.digitize(var, np.histogram(var, bins=bins)[1])

    return var