def admin_print_styles(request):
    """
    Returns a dictionary of all unique print_styles, and their latest tag,
    revision, and recipe_type.
    """
    styles = []
    # This fetches all recipes that have been used to successfully bake a
    # current book plus all default recipes that have not yet been used
    # as well as "bad" books that are not "current" state, but would otherwise
    # be the latest/current for that book
    with db_connect(cursor_factory=DictCursor) as db_conn:
        with db_conn.cursor() as cursor:
            cursor.execute("""\
                WITH latest AS (SELECT print_style, recipe,
                    count(*), count(nullif(stateid, 1)) as bad
                FROM modules m
                WHERE portal_type = 'Collection'
                      AND recipe IS NOT NULL
                      AND (
                          baked IS NOT NULL OR (
                              baked IS NULL AND stateid not in (1,8)
                              )
                          )
                      AND ARRAY [major_version, minor_version] = (
                          SELECT max(ARRAY[major_version,minor_version]) FROM
                              modules where m.uuid= uuid)

                GROUP BY print_style, recipe
                ),
                defaults AS (SELECT print_style, fileid AS recipe
                FROM default_print_style_recipes d
                WHERE not exists (SELECT 1
                                  FROM latest WHERE latest.recipe = d.fileid)
                )
                SELECT coalesce(ps.print_style, '(custom)') as print_style,
                       ps.title, coalesce(ps.recipe_type, 'web') as type,
                       ps.revised, ps.tag, ps.commit_id, la.count, la.bad
                FROM latest la LEFT JOIN print_style_recipes ps ON
                                    la.print_style = ps.print_style AND
                                    la.recipe = ps.fileid
                UNION ALL
                SELECT ps.print_style, ps.title, ps.recipe_type,
                       ps.revised, ps.tag, ps.commit_id, 0 AS count, 0 AS bad
                FROM defaults de JOIN print_style_recipes ps ON
                                    de.print_style = ps.print_style AND
                                    de.recipe = ps.fileid

            ORDER BY revised desc NULLS LAST, print_style

                """)
            for row in cursor.fetchall():
                styles.append({
                    'print_style': row['print_style'],
                    'title': row['title'],
                    'type': row['type'],
                    'revised': row['revised'],
                    'tag': row['tag'],
                    'commit_id': row['commit_id'],
                    'number': row['count'],
                    'bad': row['bad'],
                    'link': request.route_path('admin-print-style-single',
                                               style=row['print_style'])
                })
    return {'styles': styles}