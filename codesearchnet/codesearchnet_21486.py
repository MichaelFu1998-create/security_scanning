def _get_column_nums_from_args(columns):
    """Turn column inputs from user into list of simple numbers.

    Inputs can be:

      - individual number: 1
      - range: 1-3
      - comma separated list: 1,2,3,4-6
    """
    nums = []
    for c in columns:
        for p in c.split(','):
            p = p.strip()
            try:
                c = int(p)
                nums.append(c)
            except (TypeError, ValueError):
                start, ignore, end = p.partition('-')
                try:
                    start = int(start)
                    end = int(end)
                except (TypeError, ValueError):
                    raise ValueError(
                        'Did not understand %r, expected digit-digit' % c
                    )
                inc = 1 if start < end else -1
                nums.extend(range(start, end + inc, inc))
    # The user will pass us 1-based indexes, but we need to use
    # 0-based indexing with the row.
    return [n - 1 for n in nums]