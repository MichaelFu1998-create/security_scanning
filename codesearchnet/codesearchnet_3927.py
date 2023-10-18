def group_items(items, groupids):
    r"""
    Groups a list of items by group id.

    Args:
        items (Iterable): a list of items to group
        groupids (Iterable or Callable): a corresponding list of item groupids
            or a function mapping an item to a groupid.

    Returns:
        dict: groupid_to_items: maps a groupid to a list of items

    CommandLine:
        python -m ubelt.util_dict group_items

    Example:
        >>> import ubelt as ub
        >>> items    = ['ham',     'jam',   'spam',     'eggs',    'cheese', 'banana']
        >>> groupids = ['protein', 'fruit', 'protein',  'protein', 'dairy',  'fruit']
        >>> groupid_to_items = ub.group_items(items, groupids)
        >>> print(ub.repr2(groupid_to_items, nl=0))
        {'dairy': ['cheese'], 'fruit': ['jam', 'banana'], 'protein': ['ham', 'spam', 'eggs']}
    """
    if callable(groupids):
        keyfunc = groupids
        pair_list = ((keyfunc(item), item) for item in items)
    else:
        pair_list = zip(groupids, items)

    # Initialize a dict of lists
    groupid_to_items = defaultdict(list)
    # Insert each item into the correct group
    for key, item in pair_list:
        groupid_to_items[key].append(item)
    return groupid_to_items