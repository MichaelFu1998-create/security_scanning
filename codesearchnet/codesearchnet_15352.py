def delete_acl_request(request):
    """Submission to remove an ACL."""
    uuid_ = request.matchdict['uuid']

    posted = request.json
    permissions = [(x['uid'], x['permission'],) for x in posted]
    with db_connect() as db_conn:
        with db_conn.cursor() as cursor:
            remove_acl(cursor, uuid_, permissions)

    resp = request.response
    resp.status_int = 200
    return resp