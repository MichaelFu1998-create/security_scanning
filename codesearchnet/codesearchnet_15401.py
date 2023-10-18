def upsert_role_requests(cursor, uuid_, roles):
    """Given a ``uuid`` and list of dicts containing the ``uid`` and
    ``role`` for creating a role acceptance entry. The ``roles`` dict
    can optionally contain a ``has_accepted`` value, which will default
    to true.
    """
    if not isinstance(roles, (list, set, tuple,)):
        raise TypeError("``roles`` is an invalid type: {}"
                        .format(type(roles)))

    acceptors = set([(x['uid'], x['role'],) for x in roles])

    # Acquire a list of existing acceptors.
    cursor.execute("""\
SELECT user_id, role_type, accepted
FROM role_acceptances
WHERE uuid = %s""", (uuid_,))
    existing_roles = cursor.fetchall()

    # Who's not in the existing list?
    existing_acceptors = set([(r, t,) for r, t, _ in existing_roles])
    new_acceptors = acceptors.difference(existing_acceptors)

    # Insert the new role acceptors.
    for acceptor, type_ in new_acceptors:
        has_accepted = [x.get('has_accepted', None)
                        for x in roles
                        if acceptor == x['uid'] and type_ == x['role']][0]
        cursor.execute("""\
INSERT INTO role_acceptances ("uuid", "user_id", "role_type", "accepted")
VALUES (%s, %s, %s, %s)""", (uuid_, acceptor, type_, has_accepted,))

    # Update any existing license acceptors
    acceptors = set([
        (x['uid'], x['role'], x.get('has_accepted', None),)
        for x in roles
        # Prevent updating newly inserted records.
        if (x['uid'], x.get('has_accepted', None),) not in new_acceptors
    ])
    existing_acceptors = set([
        x for x in existing_roles
        # Prevent updating newly inserted records.
        if (x[0], x[1],) not in new_acceptors
    ])
    tobe_updated_acceptors = acceptors.difference(existing_acceptors)

    for uid, type_, has_accepted in tobe_updated_acceptors:
        cursor.execute("""\
UPDATE role_acceptances SET accepted = %s
WHERE uuid = %s AND user_id = %s AND role_type = %s""",
                       (has_accepted, uuid_, uid, type_,))