def remove_role_requests(cursor, uuid_, roles):
    """Given a ``uuid`` and list of dicts containing the ``uid``
    (user identifiers) and ``role`` for removal of the identified
    users' role acceptance entries.
    """
    if not isinstance(roles, (list, set, tuple,)):
        raise TypeError("``roles`` is an invalid type: {}".format(type(roles)))

    acceptors = set([(x['uid'], x['role'],) for x in roles])

    # Remove the the entries.
    for uid, role_type in acceptors:
        cursor.execute("""\
DELETE FROM role_acceptances
WHERE uuid = %s AND user_id = %s AND role_type = %s""",
                       (uuid_, uid, role_type,))