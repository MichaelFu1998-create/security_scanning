def get_default_key_store(*args, config, **kwargs):
    """ This method returns the default **key** store
        that uses an SQLite database internally.

        :params str appname: The appname that is used internally to distinguish
            different SQLite files
    """
    kwargs["appname"] = kwargs.get("appname", "graphene")
    return SqliteEncryptedKeyStore(config=config, **kwargs)