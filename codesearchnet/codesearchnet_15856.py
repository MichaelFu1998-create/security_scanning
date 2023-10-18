def _find_first_bigger(self, timestamps, target, lower_bound, upper_bound):
    """
    Find the first element in timestamps whose value is bigger than target.
    param list values: list of timestamps(epoch number).
    param target: target value.
    param lower_bound: lower bound for binary search.
    param upper_bound: upper bound for binary search.
    """
    while lower_bound < upper_bound:
      pos = lower_bound + (upper_bound - lower_bound) / 2
      if timestamps[pos] > target:
        upper_bound = pos
      else:
        lower_bound = pos + 1
    return pos