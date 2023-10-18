def _insert_metadata(cursor, model, publisher, message):
    """Insert a module with the given ``metadata``."""
    params = model.metadata.copy()
    params['publisher'] = publisher
    params['publication_message'] = message
    params['_portal_type'] = _model_to_portaltype(model)

    params['summary'] = str(cnxepub.DocumentSummaryFormatter(model))

    # Transform person structs to id lists for database array entry.
    for person_field in ATTRIBUTED_ROLE_KEYS:
        params[person_field] = [parse_user_uri(x['id'])
                                for x in params.get(person_field, [])]
    params['parent_ident_hash'] = parse_parent_ident_hash(model)

    # Assign the id and version if one is known.
    if model.ident_hash is not None:
        uuid, version = split_ident_hash(model.ident_hash,
                                         split_version=True)
        params['_uuid'] = uuid
        params['_major_version'], params['_minor_version'] = version
        # Lookup legacy ``moduleid``.
        cursor.execute("SELECT moduleid FROM latest_modules WHERE uuid = %s",
                       (uuid,))
        # There is the chance that a uuid and version have been set,
        #   but a previous publication does not exist. Therefore the
        #   moduleid will not be found. This happens on a pre-publication.
        try:
            moduleid = cursor.fetchone()[0]
        except TypeError:  # NoneType
            moduleid = None
        params['_moduleid'] = moduleid

        # Verify that uuid is reserved in document_contols. If not, add it.
        cursor.execute("SELECT * from document_controls where uuid = %s",
                       (uuid,))
        try:
            cursor.fetchone()[0]
        except TypeError:  # NoneType
            cursor.execute("INSERT INTO document_controls (uuid) VALUES (%s)",
                           (uuid,))

        created = model.metadata.get('created', None)
        # Format the statement to accept the identifiers.
        stmt = MODULE_INSERTION_TEMPLATE.format(**{
            '__uuid__': "%(_uuid)s::uuid",
            '__major_version__': "%(_major_version)s",
            '__minor_version__': "%(_minor_version)s",
            '__moduleid__': moduleid is None and "DEFAULT" or "%(_moduleid)s",
            '__created__': created is None and "DEFAULT" or "%(created)s",
        })
    else:
        created = model.metadata.get('created', None)
        # Format the statement for defaults.
        stmt = MODULE_INSERTION_TEMPLATE.format(**{
            '__uuid__': "DEFAULT",
            '__major_version__': "DEFAULT",
            '__minor_version__': "DEFAULT",
            '__moduleid__': "DEFAULT",
            '__created__': created is None and "DEFAULT" or "%(created)s",
        })

    # Insert the metadata
    cursor.execute(stmt, params)
    module_ident, ident_hash = cursor.fetchone()
    # Insert optional roles
    _insert_optional_roles(cursor, model, module_ident)

    return module_ident, ident_hash