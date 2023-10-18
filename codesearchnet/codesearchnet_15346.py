def delete_license_request(request):
    """Submission to remove a license acceptance request."""
    uuid_ = request.matchdict['uuid']

    posted_uids = [x['uid'] for x in request.json.get('licensors', [])]
    with db_connect() as db_conn:
        with db_conn.cursor() as cursor:
            remove_license_requests(cursor, uuid_, posted_uids)

    resp = request.response
    resp.status_int = 200
    return resp