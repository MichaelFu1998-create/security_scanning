def bake_content(request):
    """Invoke the baking process - trigger post-publication"""
    ident_hash = request.matchdict['ident_hash']
    try:
        id, version = split_ident_hash(ident_hash)
    except IdentHashError:
        raise httpexceptions.HTTPNotFound()

    if not version:
        raise httpexceptions.HTTPBadRequest('must specify the version')

    with db_connect() as db_conn:
        with db_conn.cursor() as cursor:
            cursor.execute("""\
SELECT bool(portal_type = 'Collection'), stateid, module_ident
FROM modules
WHERE ident_hash(uuid, major_version, minor_version) = %s
""", (ident_hash,))
            try:
                is_binder, stateid, module_ident = cursor.fetchone()
            except TypeError:
                raise httpexceptions.HTTPNotFound()
            if not is_binder:
                raise httpexceptions.HTTPBadRequest(
                    '{} is not a book'.format(ident_hash))

            if stateid == 5:
                cursor.execute("""\
SELECT pg_notify('post_publication',
'{"module_ident": '||%s||',
  "ident_hash": "'||%s||'",
  "timestamp": "'||CURRENT_TIMESTAMP||'"}')
""", (module_ident, ident_hash))
            else:
                cursor.execute("""\
UPDATE modules SET stateid = 5
WHERE ident_hash(uuid, major_version, minor_version) = %s
""", (ident_hash,))