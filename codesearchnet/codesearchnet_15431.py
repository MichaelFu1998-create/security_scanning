def get_previous_publication(cursor, ident_hash):
    """Get the previous publication of the given
    publication as an ident-hash.
    """
    cursor.execute("""\
WITH contextual_module AS (
  SELECT uuid, module_ident
  FROM modules
  WHERE ident_hash(uuid, major_version, minor_version) = %s)
SELECT ident_hash(m.uuid, m.major_version, m.minor_version)
FROM modules AS m JOIN contextual_module AS context ON (m.uuid = context.uuid)
WHERE
  m.module_ident < context.module_ident
ORDER BY revised DESC
LIMIT 1""", (ident_hash,))
    try:
        previous_ident_hash = cursor.fetchone()[0]
    except TypeError:  # NoneType
        previous_ident_hash = None
    return previous_ident_hash