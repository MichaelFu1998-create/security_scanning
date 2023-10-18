def plot_stoch_vol(data, trace=None, ax=None):
    """
    Generate plot for stochastic volatility model.

    Parameters
    ----------
    data : pandas.Series
        Returns to model.
    trace : pymc3.sampling.BaseTrace object, optional
        trace as returned by model_stoch_vol
        If not passed, sample from model.
    ax : matplotlib.axes object, optional
        Plot into axes object

    Returns
    -------
    ax object

    See Also
    --------
    model_stoch_vol : run stochastic volatility model
    """

    if trace is None:
        trace = model_stoch_vol(data)

    if ax is None:
        fig, ax = plt.subplots(figsize=(15, 8))

    data.abs().plot(ax=ax)
    ax.plot(data.index, np.exp(trace['s', ::30].T), 'r', alpha=.03)
    ax.set(title='Stochastic volatility', xlabel='Time', ylabel='Volatility')
    ax.legend(['Abs returns', 'Stochastic volatility process'],
              frameon=True, framealpha=0.5)

    return ax