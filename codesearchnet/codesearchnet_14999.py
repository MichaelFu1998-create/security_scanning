def servicestore_factory(registry, database=None):
    """
    Creates a service store with the interface of :class:`twitcher.store.ServiceStore`.
    By default the mongodb implementation will be used.

    :return: An instance of :class:`twitcher.store.ServiceStore`.
    """
    database = database or 'mongodb'
    if database == 'mongodb':
        db = _mongodb(registry)
        store = MongodbServiceStore(collection=db.services)
    else:
        store = MemoryServiceStore()
    return store