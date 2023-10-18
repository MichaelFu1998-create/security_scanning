def delete_roles_request(request):
    """Submission to remove a role acceptance request."""
    uuid_ = request.matchdict['uuid']

    posted_roles = request.json
    with db_connect() as db_conn:
        with db_conn.cursor() as cursor:
            remove_role_requests(cursor, uuid_, posted_roles)

    resp = request.response
    resp.status_int = 200
    return resp