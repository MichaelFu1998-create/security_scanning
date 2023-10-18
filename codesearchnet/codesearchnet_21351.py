def update(self, fieldname, localValue, remoteValue):
    '''
    Returns the appropriate current value, based on the changes
    recorded by this ChangeTracker, the value stored by the server
    (`localValue`), and the value stored by the synchronizing client
    (`remoteValue`). If `remoteValue` conflicts with changes stored
    locally, then a `pysyncml.ConflictError` is raised.

    If a change needs to be applied because `remoteValue` has been
    updated, then the new value will be returned, and this
    ChangeTracker will be updated such that a call to
    :meth:`getChangeSpec` will incorporate the change.

    :param fieldname:

      The name of the fieldname being evaluated.

    :param localValue:

      The value of the field as stored by the server, usually the one that
      also stored the current change-spec. If `localValue` is ``None``,
      then it is assumed that the field was potentially added (this will
      first be verified against the stored change-spec).

    :param remoteValue:

      The new value being presented that may or may not be a source of
      conflict. If `remoteValue` is ``None``, then it is assumed that
      the field was potentially deleted (this will first be verified
      against the stored change-spec).

    '''
    if localValue == remoteValue:
      return localValue
    ct = constants.ITEM_DELETED if remoteValue is None else constants.ITEM_MODIFIED
    if localValue is None:
      ct = constants.ITEM_ADDED

    # todo: i should probably trap irep errors. for example, if this
    #       cspec has a field "x" marked as deleted, then `localValue`
    #       must be None... etc.

    # TODO: i think this kind of handling would break in ListChangeTracker!...

    changed = self.isChange(fieldname, ct, remoteValue)
    if changed is None:
      return localValue
    self.append(changed, ct, initialValue=localValue, isMd5=False)
    return remoteValue