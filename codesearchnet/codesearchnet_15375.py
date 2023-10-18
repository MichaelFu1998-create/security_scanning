def upsert_pending_roles(cursor, document_id):
    """Update or insert records for pending document role acceptance."""
    cursor.execute("""\
SELECT "uuid", "metadata"
FROM pending_documents
WHERE id = %s""", (document_id,))
    uuid_, metadata = cursor.fetchone()

    acceptors = set([(uid, _role_type_to_db_type(type_),)
                     for uid, type_ in _dissect_roles(metadata)])

    # Upsert the user info.
    upsert_users(cursor, [x[0] for x in acceptors])

    # Acquire a list of existing acceptors.
    cursor.execute("""\
SELECT user_id, role_type
FROM role_acceptances
WHERE uuid = %s""", (uuid_,))
    existing_roles = set([(r, t,) for r, t in cursor.fetchall()])

    # Who's not in the existing list?
    existing_acceptors = existing_roles
    new_acceptors = acceptors.difference(existing_acceptors)

    # Insert the new role acceptors.
    for acceptor, type_ in new_acceptors:
        cursor.execute("""\
INSERT INTO role_acceptances
  ("uuid", "user_id", "role_type", "accepted")
        VALUES (%s, %s, %s, DEFAULT)""", (uuid_, acceptor, type_))

    # Has everyone already accepted?
    cursor.execute("""\
SELECT user_id
FROM role_acceptances
WHERE
  uuid = %s
  AND
  (accepted is UNKNOWN OR accepted is FALSE)""", (uuid_,))
    defectors = set(cursor.fetchall())

    if not defectors:
        # Update the pending document license acceptance state.
        cursor.execute("""\
update pending_documents set roles_accepted = 't'
where id = %s""", (document_id,))