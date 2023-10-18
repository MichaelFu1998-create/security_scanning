def _update(obj, fields=None, save=False, overwrite=False):
    """Update/populate any database fields that have `_get`ters to populate them with, regardless of whether they are data fields or related fields"""
    if not fields:
        meta = obj._meta
        fields = [f.name for f in meta.fields if not f.primary_key and hasattr(meta, '_get_' + f.name) and hasattr(meta, '_' + f.name)]
    # print fields
    fields_updated = []
    for field in fields:
        # skip fields if they contain non-null data and `overwrite` option wasn't set
        if not overwrite and not getattr(obj, field, None) == None:
            # print 'skipping %s which already has a value of %s' % (field, getattr(obj, field, None))
            continue
        # print field
        if hasattr(obj, field):
            # print field, getattr(obj, '_' + field, None)
            setattr(obj, field, getattr(obj, '_' + field, None))
            if getattr(obj, field, None) != None:
                fields_updated += [field]
    if save:
        obj.save()
    return fields_updated