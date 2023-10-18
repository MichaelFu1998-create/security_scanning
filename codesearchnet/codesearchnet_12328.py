def _single_true(iterable):
    '''This returns True if only one True-ish element exists in `iterable`.

    Parameters
    ----------

    iterable : iterable

    Returns
    -------

    bool
        True if only one True-ish element exists in `iterable`. False otherwise.

    '''

    # return True if exactly one true found
    iterator = iter(iterable)

    # consume from "i" until first true or it's exhausted
    has_true = any(iterator)

    # carry on consuming until another true value / exhausted
    has_another_true = any(iterator)

    return has_true and not has_another_true