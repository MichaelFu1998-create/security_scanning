def _validate_derived_from(cursor, model):
    """Given a database cursor and model, check the derived-from
    value accurately points to content in the archive.
    The value can be nothing or must point to existing content.
    """
    derived_from_uri = model.metadata.get('derived_from_uri')
    if derived_from_uri is None:
        return  # bail out early

    # Can we parse the value?
    try:
        ident_hash = parse_archive_uri(derived_from_uri)
        uuid_, version = split_ident_hash(ident_hash, split_version=True)
    except (ValueError, IdentHashSyntaxError, IdentHashShortId) as exc:
        raise exceptions.InvalidMetadata('derived_from_uri', derived_from_uri,
                                         original_exception=exc)
    # Is the ident-hash a valid pointer?
    args = [uuid_]
    table = 'modules'
    version_condition = ''
    if version != (None, None,):
        args.extend(version)
        table = 'modules'
        version_condition = " AND major_version = %s" \
                            " AND minor_version {} %s" \
                            .format(version[1] is None and 'is' or '=')
    cursor.execute("""SELECT 't' FROM {} WHERE uuid::text = %s{}"""
                   .format(table, version_condition), args)
    try:
        _exists = cursor.fetchone()[0]  # noqa
    except TypeError:  # None type
        raise exceptions.InvalidMetadata('derived_from_uri', derived_from_uri)

    # Assign the derived_from value so that we don't have to split it again.
    model.metadata['derived_from'] = ident_hash