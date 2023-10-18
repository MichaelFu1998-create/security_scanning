def matchItem(self, item):
    '''
    [OPTIONAL] Attempts to find the specified item and returns an item
    that describes the same object although it's specific properties
    may be different. For example, a contact whose name is an
    identical match, but whose telephone number has changed would
    return the matched item. ``None`` should be returned if no match
    is found, otherwise the item that `item` matched should be
    returned.

    This is used primarily when a slow-sync is invoked and objects
    that exist in both peers should not be replicated.

    Note that **NO** merging of the items' properties should be done;
    that will be initiated via a separate call to :meth:`mergeItems`.

    This method by default will iterate over all items (by calling
    :meth:`getAllItems`) and compare them using ``cmp()``. This means
    that if the items managed by this agent implement the ``__eq__``
    or ``__cmp__`` methods, then matching items will be detected and
    returned. Otherwise, any items that exist in both peers will be
    duplicated on slow-sync.

    Sub-classes *should* implement a more efficient method of finding
    matching items.

    See :doc:`../merging` for details.
    '''
    for match in self.getAllItems():
      if cmp(match, item) == 0:
        return match
    return None