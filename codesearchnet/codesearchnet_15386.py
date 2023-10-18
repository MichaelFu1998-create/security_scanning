def set_publication_failure(cursor, exc):
    """Given a publication exception, set the publication as failed and
    append the failure message to the publication record.
    """
    publication_id = exc.publication_id
    if publication_id is None:
        raise ValueError("Exception must have a ``publication_id`` value.")
    cursor.execute("""\
SELECT "state_messages"
FROM publications
WHERE id = %s""", (publication_id,))
    state_messages = cursor.fetchone()[0]
    if state_messages is None:
        state_messages = []
    entry = exc.__dict__
    entry['message'] = exc.message
    state_messages.append(entry)
    state_messages = json.dumps(state_messages)
    cursor.execute("""\
UPDATE publications SET ("state", "state_messages") = (%s, %s)
WHERE id = %s""", ('Failed/Error', state_messages, publication_id,))