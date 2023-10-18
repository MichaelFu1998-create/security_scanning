def publish_model(cursor, model, publisher, message):
    """Publishes the ``model`` and return its ident_hash."""
    publishers = publisher
    if isinstance(publishers, list) and len(publishers) > 1:
        raise ValueError("Only one publisher is allowed. '{}' "
                         "were given: {}"
                         .format(len(publishers), publishers))
    module_ident, ident_hash = _insert_metadata(cursor, model,
                                                publisher, message)

    for resource in getattr(model, 'resources', []):
        _insert_resource_file(cursor, module_ident, resource)

    if isinstance(model, Document):
        html = bytes(cnxepub.DocumentContentFormatter(model))
        sha1 = hashlib.new('sha1', html).hexdigest()
        cursor.execute("SELECT fileid FROM files WHERE sha1 = %s", (sha1,))
        try:
            fileid = cursor.fetchone()[0]
        except TypeError:
            file_args = {
                'media_type': 'text/html',
                'data': psycopg2.Binary(html),
            }
            cursor.execute("""\
            insert into files (file, media_type)
            VALUES (%(data)s, %(media_type)s)
            returning fileid""", file_args)
            fileid = cursor.fetchone()[0]
        args = {
            'module_ident': module_ident,
            'filename': 'index.cnxml.html',
            'fileid': fileid,
        }
        cursor.execute("""\
        INSERT INTO module_files
          (module_ident, fileid, filename)
        VALUES
          (%(module_ident)s, %(fileid)s, %(filename)s)""", args)

    elif isinstance(model, Binder):
        tree = cnxepub.model_to_tree(model)
        tree = _insert_tree(cursor, tree)
    return ident_hash