def remove_license_requests(cursor, uuid_, uids):
    """Given a ``uuid`` and list of ``uids`` (user identifiers)
    remove the identified users' license acceptance entries.
    """
    if not isinstance(uids, (list, set, tuple,)):
        raise TypeError("``uids`` is an invalid type: {}".format(type(uids)))

    acceptors = list(set(uids))

    # Remove the the entries.
    cursor.execute("""\
DELETE FROM license_acceptances
WHERE uuid = %s AND user_id = ANY(%s::text[])""", (uuid_, acceptors,))