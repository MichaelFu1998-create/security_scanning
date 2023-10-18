def get_roles_request(request):
    """Returns a list of accepting roles."""
    uuid_ = request.matchdict['uuid']
    user_id = request.matchdict.get('uid')

    args = [uuid_]
    if user_id is not None:
        fmt_conditional = "AND user_id = %s"
        args.append(user_id)
    else:
        fmt_conditional = ""

    with db_connect() as db_conn:
        with db_conn.cursor() as cursor:
            cursor.execute("""\
SELECT row_to_json(combined_rows) FROM (
SELECT uuid, user_id AS uid, role_type AS role, accepted AS has_accepted
FROM role_acceptances AS la
WHERE uuid = %s {}
ORDER BY user_id ASC, role_type ASC
) as combined_rows""".format(fmt_conditional), args)
            acceptances = [r[0] for r in cursor.fetchall()]

            if not acceptances:
                if user_id is not None:
                    raise httpexceptions.HTTPNotFound()
                else:
                    cursor.execute("""\
SELECT TRUE FROM document_controls WHERE uuid = %s""", (uuid_,))
                    try:
                        cursor.fetchone()[0]
                    except TypeError:  # NoneType
                        raise httpexceptions.HTTPNotFound()

    resp_value = acceptances
    if user_id is not None:
        resp_value = acceptances[0]
    return resp_value