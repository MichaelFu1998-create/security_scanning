def admin_content_status(request):
    """
    Returns a dictionary with the states and info of baking books,
    and the filters from the GET request to pre-populate the form.
    """
    statement, sql_args = get_baking_statuses_sql(request.GET)

    states = []
    status_filters = request.params.getall('status_filter') or []
    state_icons = dict(STATE_ICONS)
    with db_connect(cursor_factory=DictCursor) as db_conn:
        with db_conn.cursor() as cursor:
            cursor.execute(statement, vars=sql_args)
            for row in cursor.fetchall():
                message = ''
                state = row['state'] or 'PENDING'
                if status_filters and state not in status_filters:
                    continue
                if state == 'FAILURE':  # pragma: no cover
                    if row['traceback'] is not None:
                        message = row['traceback'].split("\n")[-2]
                latest_recipe = row['latest_recipe_id']
                current_recipe = row['recipe_id']
                if (current_recipe is not None and
                        current_recipe != latest_recipe):
                    state += ' stale_recipe'
                state_icon = state
                if state[:7] == "SUCCESS" and len(state) > 7:
                    state_icon = 'unknown'
                states.append({
                    'title': row['name'].decode('utf-8'),
                    'authors': format_authors(row['authors']),
                    'uuid': row['uuid'],
                    'print_style': row['print_style'],
                    'print_style_link': request.route_path(
                        'admin-print-style-single', style=row['print_style']),
                    'recipe': row['recipe'],
                    'recipe_name': row['recipe_name'],
                    'recipe_tag': row['recipe_tag'],
                    'recipe_link': request.route_path(
                        'get-resource', hash=row['recipe']),
                    'created': row['created'],
                    'state': state,
                    'state_message': message,
                    'state_icon': state_icons.get(
                        state_icon, DEFAULT_ICON),
                    'status_link': request.route_path(
                        'admin-content-status-single', uuid=row['uuid']),
                    'content_link': request.route_path(
                        'get-content', ident_hash=row['ident_hash'])
                })
    sort = request.params.get('sort', 'bpsa.created DESC')
    sort_match = SORTS_DICT[sort.split(' ')[0]]
    sort_arrow = ARROW_MATCH[sort.split(' ')[1]]
    if sort == "STATE ASC":
        states.sort(key=lambda x: x['state'])
    if sort == "STATE DESC":
        states.sort(key=lambda x: x['state'], reverse=True)

    num_entries = request.params.get('number', 100) or 100
    page = request.params.get('page', 1) or 1
    try:
        page = int(page)
        num_entries = int(num_entries)
        start_entry = (page - 1) * num_entries
    except ValueError:
        raise httpexceptions.HTTPBadRequest(
            'invalid page({}) or entries per page({})'.
            format(page, num_entries))
    total_entries = len(states)
    states = states[start_entry: start_entry + num_entries]

    returns = sql_args
    returns.update({'start_entry': start_entry,
                    'num_entries': num_entries,
                    'page': page,
                    'total_entries': total_entries,
                    'states': states,
                    'sort_' + sort_match: sort_arrow,
                    'sort': sort,
                    'domain': request.host,
                    'latest_only': request.GET.get('latest', False),
                    'STATE_ICONS': STATE_ICONS,
                    'status_filters': status_filters or [
                        i[0] for i in STATE_ICONS]})
    return returns