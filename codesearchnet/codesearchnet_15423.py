def _insert_file(cursor, file, media_type):
    """Upsert the ``file`` and ``media_type`` into the files table.
    Returns the ``fileid`` and ``sha1`` of the upserted file.

    """
    resource_hash = _get_file_sha1(file)
    cursor.execute("SELECT fileid FROM files WHERE sha1 = %s",
                   (resource_hash,))
    try:
        fileid = cursor.fetchone()[0]
    except (IndexError, TypeError):
        cursor.execute("INSERT INTO files (file, media_type) "
                       "VALUES (%s, %s)"
                       "RETURNING fileid",
                       (psycopg2.Binary(file.read()), media_type,))
        fileid = cursor.fetchone()[0]
    return fileid, resource_hash