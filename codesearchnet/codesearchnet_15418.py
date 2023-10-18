def admin_content_status_single(request):
    """
    Returns a dictionary with all the past baking statuses of a single book.
    """
    uuid = request.matchdict['uuid']
    try:
        UUID(uuid)
    except ValueError:
        raise httpexceptions.HTTPBadRequest(
            '{} is not a valid uuid'.format(uuid))

    statement, sql_args = get_baking_statuses_sql({'uuid': uuid})
    with db_connect(cursor_factory=DictCursor) as db_conn:
        with db_conn.cursor() as cursor:
            cursor.execute(statement, sql_args)
            modules = cursor.fetchall()
            if len(modules) == 0:
                raise httpexceptions.HTTPBadRequest(
                    '{} is not a book'.format(uuid))

            states = []
            collection_info = modules[0]

            for row in modules:
                message = ''
                state = row['state'] or 'PENDING'
                if state == 'FAILURE':  # pragma: no cover
                    if row['traceback'] is not None:
                        message = row['traceback']
                latest_recipe = row['latest_recipe_id']
                current_recipe = row['recipe_id']
                if (latest_recipe is not None and
                        current_recipe != latest_recipe):
                    state += ' stale_recipe'
                states.append({
                    'version': row['current_version'],
                    'recipe': row['recipe'],
                    'created': str(row['created']),
                    'state': state,
                    'state_message': message,
                })

    return {'uuid': str(collection_info['uuid']),
            'title': collection_info['name'].decode('utf-8'),
            'authors': format_authors(collection_info['authors']),
            'print_style': collection_info['print_style'],
            'current_recipe': collection_info['recipe_id'],
            'current_ident': collection_info['module_ident'],
            'current_state': states[0]['state'],
            'states': states}