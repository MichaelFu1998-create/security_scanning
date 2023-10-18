def publish_collated_document(cursor, model, parent_model):
    """Publish a given `module`'s collated content in the context of
    the `parent_model`. Note, the model's content is expected to already
    have the collated content. This will just persist that content to
    the archive.

    """
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
        INSERT INTO files (file, media_type)
        VALUES (%(data)s, %(media_type)s)
        RETURNING fileid""", file_args)
        fileid = cursor.fetchone()[0]
    args = {
        'module_ident_hash': model.ident_hash,
        'parent_ident_hash': parent_model.ident_hash,
        'fileid': fileid,
    }
    stmt = """\
INSERT INTO collated_file_associations (context, item, fileid)
VALUES
  ((SELECT module_ident FROM modules
    WHERE ident_hash(uuid, major_version, minor_version)
   = %(parent_ident_hash)s),
   (SELECT module_ident FROM modules
    WHERE ident_hash(uuid, major_version, minor_version)
   = %(module_ident_hash)s),
   %(fileid)s)"""
    cursor.execute(stmt, args)