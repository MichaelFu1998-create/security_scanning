def publish_composite_model(cursor, model, parent_model, publisher, message):
    """Publishes the ``model`` and return its ident_hash."""
    if not (isinstance(model, CompositeDocument) or
            (isinstance(model, Binder) and
                model.metadata.get('type') == 'composite-chapter')):
        raise ValueError("This function only publishes Composite"
                         "objects. '{}' was given.".format(type(model)))
    if issequence(publisher) and len(publisher) > 1:
        raise ValueError("Only one publisher is allowed. '{}' "
                         "were given: {}"
                         .format(len(publisher), publisher))
    module_ident, ident_hash = _insert_metadata(cursor, model,
                                                publisher, message)

    model.id, model.metadata['version'] = split_ident_hash(ident_hash)
    model.set_uri('cnx-archive', ident_hash)

    for resource in model.resources:
        _insert_resource_file(cursor, module_ident, resource)

    if isinstance(model, CompositeDocument):
        html = bytes(cnxepub.DocumentContentFormatter(model))
        fileid, _ = _insert_file(cursor, io.BytesIO(html), 'text/html')
        file_arg = {
            'module_ident': module_ident,
            'parent_ident_hash': parent_model.ident_hash,
            'fileid': fileid,
        }
        cursor.execute("""\
        INSERT INTO collated_file_associations
          (context, item, fileid)
        VALUES
          ((SELECT module_ident FROM modules
            WHERE ident_hash(uuid, major_version, minor_version)
           = %(parent_ident_hash)s),
            %(module_ident)s, %(fileid)s)""", file_arg)

    return ident_hash