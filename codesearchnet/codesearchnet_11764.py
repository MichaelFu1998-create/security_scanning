def exists(name=None, group=None, release=None, except_release=None, verbose=1):
    """
    Determines if a virtual machine instance exists.
    """
    verbose = int(verbose)
    instances = list_instances(
        name=name,
        group=group,
        release=release,
        except_release=except_release,
        verbose=verbose,
        show=verbose)
    ret = bool(instances)
    if verbose:
        print('\ninstance %s exist' % ('DOES' if ret else 'does NOT'))
    #return ret
    return instances