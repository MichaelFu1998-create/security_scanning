def check_settings_for_differences(old, new, as_bool=False, as_tri=False):
    """
    Returns a subset of the env dictionary keys that differ,
    either being added, deleted or changed between old and new.
    """

    assert not as_bool or not as_tri

    old = old or {}
    new = new or {}

    changes = set(k for k in set(new.iterkeys()).intersection(old.iterkeys()) if new[k] != old[k])
    if changes and as_bool:
        return True

    added_keys = set(new.iterkeys()).difference(old.iterkeys())
    if added_keys and as_bool:
        return True
    if not as_tri:
        changes.update(added_keys)

    deled_keys = set(old.iterkeys()).difference(new.iterkeys())
    if deled_keys and as_bool:
        return True
    if as_bool:
        return False
    if not as_tri:
        changes.update(deled_keys)

    if as_tri:
        return added_keys, changes, deled_keys

    return changes