def admin_content_status_single_POST(request):
    """ Retriggers baking for a given book. """
    args = admin_content_status_single(request)
    title = args['title']
    if args['current_state'] == 'SUCCESS':
        args['response'] = title + ' is not stale, no need to bake'
        return args

    with db_connect() as db_conn:
        with db_conn.cursor() as cursor:
            cursor.execute("SELECT stateid FROM modules WHERE module_ident=%s",
                           vars=(args['current_ident'],))
            data = cursor.fetchall()
            if len(data) == 0:
                raise httpexceptions.HTTPBadRequest(
                    'invalid module_ident: {}'.format(args['current_ident']))
            if data[0][0] == 5 or data[0][0] == 6:
                args['response'] = title + ' is already baking/set to bake'
                return args

            cursor.execute("""UPDATE modules SET stateid=5
                           WHERE module_ident=%s""",
                           vars=(args['current_ident'],))

            args['response'] = title + " set to bake!"

    return args