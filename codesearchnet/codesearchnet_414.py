def _cumulative_returns_less_costs(returns, costs):
    """
    Compute cumulative returns, less costs.
    """
    if costs is None:
        return ep.cum_returns(returns)
    return ep.cum_returns(returns - costs)