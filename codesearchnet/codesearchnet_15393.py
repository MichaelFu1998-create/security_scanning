def check_publication_state(publication_id):
    """Check the publication's current state."""
    with db_connect() as db_conn:
        with db_conn.cursor() as cursor:
            cursor.execute("""\
SELECT "state", "state_messages"
FROM publications
WHERE id = %s""", (publication_id,))
            publication_state, publication_messages = cursor.fetchone()
    return publication_state, publication_messages