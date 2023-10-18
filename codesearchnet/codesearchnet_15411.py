def get_moderation(request):
    """Return the list of publications that need moderation."""
    with db_connect() as db_conn:
        with db_conn.cursor() as cursor:
            cursor.execute("""\
SELECT row_to_json(combined_rows) FROM (
  SELECT id, created, publisher, publication_message,
         (select array_agg(row_to_json(pd))
          from pending_documents as pd
          where pd.publication_id = p.id) AS models
  FROM publications AS p
  WHERE state = 'Waiting for moderation') AS combined_rows""")
            moderations = [x[0] for x in cursor.fetchall()]

    return moderations