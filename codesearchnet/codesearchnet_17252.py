def one_sided(value: float, distribution: List[float]) -> float:
    """Calculate the one-sided probability of getting a value more extreme than the distribution."""
    assert distribution
    return sum(value < element for element in distribution) / len(distribution)