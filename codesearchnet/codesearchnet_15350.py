def get_acl(request):
    """Returns the ACL for the given content identified by ``uuid``."""
    uuid_ = request.matchdict['uuid']

    with db_connect() as db_conn:
        with db_conn.cursor() as cursor:
            cursor.execute("""\
SELECT TRUE FROM document_controls WHERE uuid = %s""", (uuid_,))
            try:
                # Check that it exists
                cursor.fetchone()[0]
            except TypeError:
                raise httpexceptions.HTTPNotFound()
            cursor.execute("""\
SELECT row_to_json(combined_rows) FROM (
SELECT uuid, user_id AS uid, permission
FROM document_acl AS acl
WHERE uuid = %s
ORDER BY user_id ASC, permission ASC
) as combined_rows""", (uuid_,))
            acl = [r[0] for r in cursor.fetchall()]

    return acl