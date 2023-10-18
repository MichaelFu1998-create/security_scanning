def get_baking_statuses_sql(get_request):
    """ Creates SQL to get info on baking books filtered from GET request.

    All books that have ever attempted to bake will be retured if they
    pass the filters in the GET request.
    If a single book has been requested to bake multiple times there will
    be a row for each of the baking attempts.
    By default the results are sorted in descending order of when they were
    requested to bake.

    N.B. The version reported for a print-style linked recipe will the the
    lowest cnx-recipes release installed that contains the exact recipe
    used to bake that book, regardless of when the book was baked relative
    to recipe releases. E.g. if a book uses the 'physics' recipe, and it is
    identical for versions 1.1, 1.2, 1.3, and 1.4, then it will be reported
    as version 1.1, even if the most recent release is tagged 1.4.
    """
    args = {}
    sort = get_request.get('sort', 'bpsa.created DESC')
    if (len(sort.split(" ")) != 2 or
            sort.split(" ")[0] not in SORTS_DICT.keys() or
            sort.split(" ")[1] not in ARROW_MATCH.keys()):
        raise httpexceptions.HTTPBadRequest(
            'invalid sort: {}'.format(sort))
    if sort == "STATE ASC" or sort == "STATE DESC":
        sort = 'bpsa.created DESC'
    uuid_filter = get_request.get('uuid', '').strip()
    author_filter = get_request.get('author', '').strip()
    latest_filter = get_request.get('latest', False)

    sql_filters = "WHERE"
    if latest_filter:
        sql_filters += """ ARRAY [m.major_version, m.minor_version] = (
         SELECT max(ARRAY[major_version,minor_version]) FROM
                   modules where m.uuid= uuid) AND """
    if uuid_filter != '':
        args['uuid'] = uuid_filter
        sql_filters += " m.uuid=%(uuid)s AND "
    if author_filter != '':
        author_filter = author_filter.decode('utf-8')
        sql_filters += " %(author)s=ANY(m.authors) "
        args["author"] = author_filter

    if sql_filters.endswith("AND "):
        sql_filters = sql_filters[:-4]
    if sql_filters == "WHERE":
        sql_filters = ""

    # FIXME  celery AsyncResult API is soooo sloow that this page takes
    # 2 min. or more to load on production.  As an workaround, this code
    # accesses the celery_taskmeta table directly. Need to remove that access
    # once we track enough state info ourselves. Want to track when queued,
    # started, ended, etc. for future monitoring of baking system performance
    # as well.
    # The 'limit 1' subselect is to ensure the "oldest identical version"
    # for recipes released as part of cnx-recipes (avoids one line per
    # identical recipe file in different releases, for a single baking job)

    statement = """
                       SELECT m.name, m.authors, m.uuid,
                       module_version(m.major_version,m.minor_version)
                          as current_version,
                       m.print_style,
                       CASE WHEN f.sha1 IS NOT NULL
                       THEN coalesce(dps.print_style,'(custom)')
                       ELSE dps.print_style
                       END AS recipe_name,
                       (select tag from print_style_recipes
                            where print_style = m.print_style
                                and fileid = m.recipe
                                order by revised asc limit 1) as recipe_tag,
                       coalesce(dps.fileid, m.recipe) as latest_recipe_id,
                       m.recipe as recipe_id,
                       f.sha1 as recipe,
                       m.module_ident,
                       ident_hash(m.uuid, m.major_version, m.minor_version),
                       bpsa.created, ctm.traceback,
                       CASE WHEN ctm.status = 'SUCCESS'
                           AND ms.statename = 'fallback'
                       THEN 'FALLBACK'
                       ELSE ctm.status
                       END as state
                FROM document_baking_result_associations AS bpsa
                INNER JOIN modules AS m USING (module_ident)
                INNER JOIN modulestates as ms USING (stateid)
                LEFT JOIN celery_taskmeta AS ctm
                    ON bpsa.result_id = ctm.task_id::uuid
                LEFT JOIN default_print_style_recipes as dps
                    ON dps.print_style = m.print_style
                LEFT JOIN latest_modules as lm
                    ON lm.uuid=m.uuid
                LEFT JOIN files f on m.recipe = f.fileid
                {}
                ORDER BY {};
                """.format(sql_filters, sort)
    args.update({'sort': sort})
    return statement, args