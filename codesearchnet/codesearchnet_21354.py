def isChange(self, listIndex, changeType, newValue=None, isMd5=False, token=None):
    '''
    Implements as specified in :meth:`.ChangeTracker.isChange` where
    the `changeObject` is a two-element tuple. The first element is
    the index at which the change should be applied, and the second
    element is an abstract token that should be passed back into this
    method at every iteration.

    IMPORTANT: unlike the AttributeChangeTracker, the
    ListChangeTracker's `isChange()` method is sensitive to order
    (which is why it uses the `changeObject` and `token`
    mechanisms. Therefore, it is important to call `isChange()`
    sequentially with all changes in the order that they occur in the
    change list.
    '''

    # THE INDEX PASSED TO ListChangeTracker.isChange() DOES NOT INCLUDE:
    #   - local deletions
    #   - remote additions

    adjust  = 0               # tracks local deletes
    token   = token           # tracks consecutive addition adjustments
    index   = int(listIndex)
    ret     = index

    # todo: this should reduce complexity later on, but something
    #       went wrong...
    # if changeType != constants.ITEM_ADDED:
    #   token = None
    # else:
    #   if token is None or token[0] != index:
    #     token = (ret, 0)
    #   token = (ret, token[1] + 1)

    # todo: this seems inefficient...
    changes = self._collapseChanges(self.baseline, self.current)

    for cur in changes:
      if cur.index > index:
        if changeType != constants.ITEM_ADDED:
          return (ret, None)
        if token is None or token[0] != index - adjust:
          token = (ret, 0)
        token = (ret, token[1] + 1)
        return (ret, token)

      if cur.index != index:
        if cur.op == constants.ITEM_DELETED:
          index  += 1
          adjust += 1
        continue

      if token is not None and token[0] == index - adjust:
        index += token[1]
        continue

      if changeType == constants.ITEM_DELETED:
        if cur.op == constants.ITEM_ADDED:
          # the field is deleted because it hasn't been added yet
          return (None, None)
        # we are requiring that the current/new values are different,
        # thus there is a collision between the added values
        raise ConflictError(
          'conflicting deletion of list index %r' % (index,))

      if changeType == constants.ITEM_ADDED:
        if token is None:
          token = (ret, 0)
        token = (ret, token[1] + 1)
        if cur.op == constants.ITEM_DELETED:
          if isMd5Equal(newValue, isMd5, cur.ival, cur.md5):
            return (None, token)
          # todo: this *could* be a del-mod *conflict*... but not
          #       *NECESSARILY* so, since it could be a
          #       del-adjacent-add, which is not a problem. in the
          #       conflict case, the resolution will cause the
          #       modified line to silently win.
          # TODO: perhaps i should err on the side of safety and
          #       issue a ConflictError?...
        return (ret, token)

      if cur.op == constants.ITEM_DELETED:
        index  += 1
        adjust += 1
        continue

      # changeType = mod, op = add/mod

      if cur.op == constants.ITEM_ADDED:
        # todo: i'm not sure if this case is even possible...
        raise ConflictError(
          'conflicting addition of list index %r' % (index,))

      # mod/mod - check initvalue

      if isMd5Equal(newValue, isMd5, cur.ival, cur.md5):
        # the new value is equal to the initial value, so this
        # line was not changed (but has local changes)
        return (None, None)
      # the new value is not equal to the initial value, which means
      # that they were both changed and/or added.
      raise ConflictError(
        'conflicting modification of list index %r' % (index,))

    if changeType != constants.ITEM_ADDED:
      return (ret, None)
    if token is None or token[0] != index - adjust:
      token = (ret, 0)
    token = (ret, token[1] + 1)
    return (ret, token)