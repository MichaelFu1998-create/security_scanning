def upsert_license_requests(cursor, uuid_, roles):
    """Given a ``uuid`` and list of ``roles`` (user identifiers)
    create a license acceptance entry. If ``has_accepted`` is supplied,
    it will be used to assign an acceptance value to all listed ``uids``.
    """
    if not isinstance(roles, (list, set, tuple,)):
        raise TypeError("``roles`` is an invalid type: {}".format(type(roles)))

    acceptors = set([x['uid'] for x in roles])

    # Acquire a list of existing acceptors.
    cursor.execute("""\
SELECT user_id, accepted FROM license_acceptances WHERE uuid = %s""",
                   (uuid_,))
    existing_acceptors = cursor.fetchall()

    # Who's not in the existing list?
    new_acceptors = acceptors.difference([x[0] for x in existing_acceptors])

    # Insert the new licensor acceptors.
    if new_acceptors:
        args = []
        values_fmt = []
        for uid in new_acceptors:
            has_accepted = [x.get('has_accepted', None)
                            for x in roles
                            if uid == x['uid']][0]
            args.extend([uuid_, uid, has_accepted])
            values_fmt.append("(%s, %s, %s)")
        values_fmt = ', '.join(values_fmt)
        cursor.execute("""\
INSERT INTO license_acceptances (uuid, user_id, accepted)
VALUES {}""".format(values_fmt), args)

    # Update any existing license acceptors
    acceptors = set([
        (x['uid'], x.get('has_accepted', None),)
        for x in roles
        # Prevent updating newly inserted records.
        if (x['uid'], x.get('has_accepted', None),) not in new_acceptors
    ])
    existing_acceptors = set([
        x for x in existing_acceptors
        # Prevent updating newly inserted records.
        if x[0] not in new_acceptors
    ])
    tobe_updated_acceptors = acceptors.difference(existing_acceptors)

    for uid, has_accepted in tobe_updated_acceptors:
        cursor.execute("""\
UPDATE license_acceptances SET accepted = %s
WHERE uuid = %s AND user_id = %s""", (has_accepted, uuid_, uid,))