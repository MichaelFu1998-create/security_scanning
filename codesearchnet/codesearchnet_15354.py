def lookup_api_key_info():
    """Given a dbapi cursor, lookup all the api keys and their information."""
    info = {}
    with db_connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(ALL_KEY_INFO_SQL_STMT)
            for row in cursor.fetchall():
                id, key, name, groups = row
                user_id = "api_key:{}".format(id)
                info[key] = dict(id=id, user_id=user_id,
                                 name=name, groups=groups)
    return info