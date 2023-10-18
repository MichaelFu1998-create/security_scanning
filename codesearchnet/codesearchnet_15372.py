def _role_type_to_db_type(type_):
    """Translates a role type (a value found in
    ``cnxepub.ATTRIBUTED_ROLE_KEYS``) to a database compatible
    value for ``role_types``.
    """
    with db_connect() as db_conn:
        with db_conn.cursor() as cursor:
            cursor.execute("""\
WITH unnested_role_types AS (
  SELECT unnest(enum_range(NULL::role_types)) as role_type
  ORDER BY role_type ASC)
SELECT array_agg(role_type)::text[] FROM unnested_role_types""")
            db_types = cursor.fetchone()[0]
    return dict(zip(cnxepub.ATTRIBUTED_ROLE_KEYS, db_types))[type_]