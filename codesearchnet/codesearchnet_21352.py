def isChange(self, fieldname, changeType, newValue=None, isMd5=False):
    '''
    Implements as specified in :meth:`.ChangeTracker.isChange` where
    the `changeObject` is simply the fieldname that needs to be
    updated with the `newValue`. Currently, this is always equal to
    `fieldname`.
    '''
    # todo: this seems inefficient...
    changes = self._collapseChanges(self.baseline, self.current)
    if fieldname not in changes:
      return fieldname
    cur = changes[fieldname]
    if changeType == constants.ITEM_DELETED:
      if cur.op == constants.ITEM_ADDED or cur.op == constants.ITEM_DELETED:
        # the field is deleted because it hasn't been added yet
        # (the check for cur.op == constants.ITEM_DELETED should
        # never be true, so just here for paranoia...)
        return None
      # we are requiring that the current/new values are different,
      # thus there is a collision between the added values
      raise ConflictError('conflicting deletion of field "%s"'
                                 % (fieldname,))

    # the `newValue` is different than the current value (otherwise
    # this method should not have been called) -- either it was added
    # or modified.

    # if it appears to be "added", then it may be because it was
    # deleted in this tracker.

    # if it appears to be "modified", then it may be because it
    # was modified in this tracker.

    # in either case, check to see if it is equal to the initial
    # value, and if it was, then there was actually no change.

    if isMd5Equal(newValue, isMd5, cur.ival, cur.md5):
      # the new value is equal to the initial value, so this
      # field was not changed (but has local changes)
      return None

    # the new value is not equal to the initial value, which means
    # that they were both changed and/or added.
    raise ConflictError(
      'conflicting addition or modification of field "%s"' % (fieldname,))