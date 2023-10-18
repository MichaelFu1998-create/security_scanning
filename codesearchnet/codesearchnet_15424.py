def _insert_resource_file(cursor, module_ident, resource):
    """Insert a resource into the modules_files table. This will
    create a new file entry or associates an existing one.
    """
    with resource.open() as file:
        fileid, _ = _insert_file(cursor, file, resource.media_type)

    # Is this file legitimately used twice within the same content?
    cursor.execute("""\
select
  (fileid = %s) as is_same_file
from module_files
where module_ident = %s and filename = %s""",
                   (fileid, module_ident, resource.filename,))
    try:
        is_same_file = cursor.fetchone()[0]
    except TypeError:  # NoneType
        is_same_file = None
    if is_same_file:
        # All is good, bail out.
        return
    elif is_same_file is not None:  # pragma: no cover
        # This means the file is not the same, but a filename
        #   conflict exists.
        # FFF At this time, it is impossible to get to this logic.
        raise Exception("filename conflict")

    args = (module_ident, fileid, resource.filename,)
    cursor.execute("""\
INSERT INTO module_files (module_ident, fileid, filename)
VALUES (%s, %s, %s)""", args)