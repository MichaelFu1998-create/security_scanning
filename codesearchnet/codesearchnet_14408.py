def env_key(key, default):
    """
    Try to get `key` from the environment.

    This mutates `key` to replace dots with underscores and makes it all
    uppercase.

        my.database.host => MY_DATABASE_HOST

    """
    env = key.upper().replace('.', '_')
    return os.environ.get(env, default)