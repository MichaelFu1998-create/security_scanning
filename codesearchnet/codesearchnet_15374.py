def upsert_pending_licensors(cursor, document_id):
    """Update or insert records for pending license acceptors."""
    cursor.execute("""\
SELECT "uuid", "metadata"
FROM pending_documents
WHERE id = %s""", (document_id,))
    uuid_, metadata = cursor.fetchone()
    acceptors = set([uid for uid, type_ in _dissect_roles(metadata)])

    # Acquire a list of existing acceptors.
    cursor.execute("""\
SELECT "user_id", "accepted"
FROM license_acceptances
WHERE uuid = %s""", (uuid_,))
    existing_acceptors_mapping = dict(cursor.fetchall())

    # Who's not in the existing list?
    existing_acceptors = set(existing_acceptors_mapping.keys())
    new_acceptors = acceptors.difference(existing_acceptors)

    # Insert the new licensor acceptors.
    for acceptor in new_acceptors:
        cursor.execute("""\
INSERT INTO license_acceptances
  ("uuid", "user_id", "accepted")
VALUES (%s, %s, NULL)""", (uuid_, acceptor,))

    # Has everyone already accepted?
    cursor.execute("""\
SELECT user_id
FROM license_acceptances
WHERE
  uuid = %s
  AND
  (accepted is UNKNOWN OR accepted is FALSE)""", (uuid_,))
    defectors = set(cursor.fetchall())

    if not defectors:
        # Update the pending document license acceptance state.
        cursor.execute("""\
update pending_documents set license_accepted = 't'
where id = %s""", (document_id,))