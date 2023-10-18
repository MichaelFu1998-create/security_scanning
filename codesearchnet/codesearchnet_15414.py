def admin_print_styles_single(request):
    """ Returns all books with any version of the given print style.

    Returns the print_style, recipe type, num books using the print_style,
    along with a dictionary of the book, author, revision date, recipe,
    tag of the print_style, and a link to the content.
    """
    style = request.matchdict['style']
    # do db search to get file id and other info on the print_style
    with db_connect(cursor_factory=DictCursor) as db_conn:
        with db_conn.cursor() as cursor:

            if style != '(custom)':
                cursor.execute("""
                    SELECT fileid, recipe_type, title
                    FROM default_print_style_recipes
                    WHERE print_style=%s
                    """, vars=(style,))
                info = cursor.fetchall()
                if len(info) < 1:
                    current_recipe = None
                    recipe_type = None
                    status = None

                else:
                    current_recipe = info[0]['fileid']
                    recipe_type = info[0]['recipe_type']
                    status = 'current'

                cursor.execute("""\
                    SELECT name, authors, lm.revised, lm.recipe, psr.tag,
                        f.sha1 as hash, psr.commit_id, uuid,
                        ident_hash(uuid, major_version, minor_version)
                    FROM modules as lm
                    LEFT JOIN print_style_recipes as psr
                    ON (psr.print_style = lm.print_style and
                        psr.fileid = lm.recipe)
                    LEFT JOIN files f ON psr.fileid = f.fileid
                    WHERE lm.print_style=%s
                    AND portal_type='Collection'
                    AND ARRAY [major_version, minor_version] = (
                        SELECT max(ARRAY[major_version,minor_version])
                        FROM modules WHERE lm.uuid = uuid)

                    ORDER BY psr.tag DESC;
                    """, vars=(style,))
            else:
                current_recipe = '(custom)'
                recipe_type = '(custom)'
                cursor.execute("""\
                    SELECT name, authors, lm.revised, lm.recipe, NULL as tag,
                        f.sha1 as hash, NULL as commit_id, uuid,
                        ident_hash(uuid, major_version, minor_version)
                    FROM modules as lm
                    JOIN files f ON lm.recipe = f.fileid
                    WHERE portal_type='Collection'
                    AND NOT EXISTS (
                        SELECT 1 from print_style_recipes psr
                        WHERE psr.fileid = lm.recipe)
                    AND ARRAY [major_version, minor_version] = (
                        SELECT max(ARRAY[major_version,minor_version])
                        FROM modules WHERE lm.uuid = uuid)
                    ORDER BY uuid, recipe, revised DESC;
                    """, vars=(style,))
                status = '(custom)'

            collections = []
            for row in cursor.fetchall():
                recipe = row['recipe']
                if (status != '(custom)' and
                        current_recipe is not None and
                        recipe != current_recipe):
                    status = 'stale'
                collections.append({
                    'title': row['name'].decode('utf-8'),
                    'authors': row['authors'],
                    'revised': row['revised'],
                    'recipe': row['hash'],
                    'recipe_link': request.route_path('get-resource',
                                                      hash=row['hash']),
                    'tag': row['tag'],
                    'ident_hash': row['ident_hash'],
                    'link': request.route_path('get-content',
                                               ident_hash=row['ident_hash']),
                    'status': status,
                    'status_link': request.route_path(
                        'admin-content-status-single', uuid=row['uuid']),

                })
    return {'number': len(collections),
            'collections': collections,
            'print_style': style,
            'recipe_type': recipe_type}