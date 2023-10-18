def post_acl_request(request):
    """Submission to create an ACL."""
    uuid_ = request.matchdict['uuid']

    posted = request.json
    permissions = [(x['uid'], x['permission'],) for x in posted]
    with db_connect() as db_conn:
        with db_conn.cursor() as cursor:
            cursor.execute("""\
SELECT TRUE FROM document_controls WHERE uuid = %s::UUID""", (uuid_,))
            try:
                # Check that it exists
                cursor.fetchone()[0]
            except TypeError:
                if request.has_permission('publish.create-identifier'):
                    cursor.execute("""\
INSERT INTO document_controls (uuid) VALUES (%s)""", (uuid_,))
                else:
                    raise httpexceptions.HTTPNotFound()
            upsert_acl(cursor, uuid_, permissions)

    resp = request.response
    resp.status_int = 202
    return resp