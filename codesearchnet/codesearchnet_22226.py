def refetch_for_update(obj):
    """Queries the database for the same object that is passed in, refetching
    its contents and runs ``select_for_update()`` to lock the corresponding
    row until the next commit.

    :param obj:
        Object to refetch
    :returns:
        Refreshed version of the object
    """
    return obj.__class__.objects.select_for_update().get(id=obj.id)