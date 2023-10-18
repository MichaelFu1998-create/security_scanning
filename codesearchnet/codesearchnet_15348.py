def post_roles_request(request):
    """Submission to create a role acceptance request."""
    uuid_ = request.matchdict['uuid']

    posted_roles = request.json
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
            try:
                upsert_users(cursor, [r['uid'] for r in posted_roles])
            except UserFetchError as exc:
                raise httpexceptions.HTTPBadRequest(exc.message)
            upsert_role_requests(cursor, uuid_, posted_roles)

    resp = request.response
    resp.status_int = 202
    return resp