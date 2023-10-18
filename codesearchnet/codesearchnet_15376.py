def obtain_licenses():
    """Obtain the licenses in a dictionary form, keyed by url."""
    with db_connect() as db_conn:
        with db_conn.cursor() as cursor:
            cursor.execute("""\
SELECT combined_row.url, row_to_json(combined_row) FROM (
  SELECT "code", "version", "name", "url", "is_valid_for_publication"
  FROM licenses) AS combined_row""")
            licenses = {r[0]: r[1] for r in cursor.fetchall()}
    return licenses