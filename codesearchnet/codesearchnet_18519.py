def _link_rels(obj, fields=None, save=False, overwrite=False):
    """Populate any database related fields (ForeignKeyField, OneToOneField) that have `_get`ters to populate them with"""
    if not fields:
        meta = obj._meta
        fields = [f.name for f in meta.fields if hasattr(f, 'do_related_class') and not f.primary_key and hasattr(meta, '_get_' + f.name) and hasattr(meta, '_' + f.name)]
    for field in fields:
        # skip fields if they contain non-null data and `overwrite` option wasn't set
        if not overwrite and not isinstance(getattr(obj, field, None), NoneType):
            # print 'skipping %s which already has a value of %s' % (field, getattr(obj, field, None))
            continue
        if hasattr(obj, field):
            setattr(obj, field, getattr(obj, '_' + field, None))
    if save:
        obj.save()
    return obj