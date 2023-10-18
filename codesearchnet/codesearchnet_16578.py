def _ratio_metric(v1, v2, **_kwargs):
    """Metric for ratio data."""
    return (((v1 - v2) / (v1 + v2)) ** 2) if v1 + v2 != 0 else 0