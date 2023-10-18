def compute_consistency_score(returns_test, preds):
    """
    Compute Bayesian consistency score.

    Parameters
    ----------
    returns_test : pd.Series
        Observed cumulative returns.
    preds : numpy.array
        Multiple (simulated) cumulative returns.

    Returns
    -------
    Consistency score
        Score from 100 (returns_test perfectly on the median line of the
        Bayesian cone spanned by preds) to 0 (returns_test completely
        outside of Bayesian cone.)
    """

    returns_test_cum = cum_returns(returns_test, starting_value=1.)
    cum_preds = np.cumprod(preds + 1, 1)

    q = [sp.stats.percentileofscore(cum_preds[:, i],
                                    returns_test_cum.iloc[i],
                                    kind='weak')
         for i in range(len(returns_test_cum))]
    # normalize to be from 100 (perfect median line) to 0 (completely outside
    # of cone)
    return 100 - np.abs(50 - np.mean(q)) / .5