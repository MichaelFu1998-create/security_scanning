def _GetNextLogCountPerToken(token):
    """Wrapper for _log_counter_per_token.

    Args:
    token: The token for which to look up the count.

    Returns:
    The number of times this function has been called with
    *token* as an argument (starting at 0)
    """
    global _log_counter_per_token  # pylint: disable=global-variable-not-assigned
    _log_counter_per_token[token] = 1 + _log_counter_per_token.get(token, -1)
    return _log_counter_per_token[token]