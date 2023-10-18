def lookup_document_pointer(ident_hash, cursor):
    """Lookup a document by id and version."""
    id, version = split_ident_hash(ident_hash, split_version=True)
    stmt = "SELECT name FROM modules WHERE uuid = %s"
    args = [id]
    if version and version[0] is not None:
        operator = version[1] is None and 'is' or '='
        stmt += " AND (major_version = %s AND minor_version {} %s)" \
            .format(operator)
        args.extend(version)
    cursor.execute(stmt, args)
    try:
        title = cursor.fetchone()[0]
    except TypeError:
        raise DocumentLookupError()
    else:
        metadata = {'title': title}
    return cnxepub.DocumentPointer(ident_hash, metadata)