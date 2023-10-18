def get_api_keys(request):
    """Return the list of API keys."""
    with db_connect() as db_conn:
        with db_conn.cursor() as cursor:
            cursor.execute("""\
SELECT row_to_json(combined_rows) FROM (
  SELECT id, key, name, groups FROM api_keys
) AS combined_rows""")
            api_keys = [x[0] for x in cursor.fetchall()]

    return api_keys