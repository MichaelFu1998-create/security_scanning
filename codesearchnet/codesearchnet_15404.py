def remove_acl(cursor, uuid_, permissions):
    """Given a ``uuid`` and a set of permissions given as a tuple
    of ``uid`` and ``permission``, remove these entries from the database.
    """
    if not isinstance(permissions, (list, set, tuple,)):
        raise TypeError("``permissions`` is an invalid type: {}"
                        .format(type(permissions)))

    permissions = set(permissions)

    # Remove the the entries.
    for uid, permission in permissions:
        cursor.execute("""\
DELETE FROM document_acl
WHERE uuid = %s AND user_id = %s AND permission = %s""",
                       (uuid_, uid, permission,))