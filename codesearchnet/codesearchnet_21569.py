def temp_db(db, name=None):
    """
    A context manager that creates a temporary database.

    Useful for automated tests.

    Parameters
    ----------
    db: object
        a preconfigured DB object
    name: str, optional
        name of the database to be created. (default: globally unique name)
    """
    if name is None:
        name = temp_name()
    db.create(name)
    if not db.exists(name):
        raise DatabaseError('failed to create database %s!')
    try:
        yield name
    finally:
        db.drop(name)
        if db.exists(name):
            raise DatabaseError('failed to drop database %s!')