def upsert_acl(cursor, uuid_, permissions):
    """Given a ``uuid`` and a set of permissions given as a
    tuple of ``uid`` and ``permission``, upsert them into the database.
    """
    if not isinstance(permissions, (list, set, tuple,)):
        raise TypeError("``permissions`` is an invalid type: {}"
                        .format(type(permissions)))

    permissions = set(permissions)

    # Acquire the existin ACL.
    cursor.execute("""\
SELECT user_id, permission
FROM document_acl
WHERE uuid = %s""", (uuid_,))
    existing = set([(r, t,) for r, t in cursor.fetchall()])

    # Who's not in the existing list?
    new_entries = permissions.difference(existing)

    # Insert the new permissions.
    for uid, permission in new_entries:
        cursor.execute("""\
INSERT INTO document_acl
  ("uuid", "user_id", "permission")
VALUES (%s, %s, %s)""", (uuid_, uid, permission))