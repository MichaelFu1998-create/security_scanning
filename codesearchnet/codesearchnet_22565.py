def validate( table, **data ):
    '''
    theoretically, any data store can be implemented to work with this package,
    which means basic data validation must be done in-package, so that weird
    stuff can't be stored in the data store.
    this function raises an exception if an invalid table name is passed, not
    all of the required fields are in the data kwargs, or if a field that was
    passed is not expected.
    it also returns the key field name, for ensuring uniqueness (again, that may
    not be built into whatever data store is impelemented.)
    '''
    if table not in good.keys():
        raise Proauth2Error( 'invalid_request', 'invalid name: %s' % table )
    for req in good[table]['required']:
        if not data.get( req, None ):
            raise Proauth2Error( 'invalid_request',
                                 'missing required field: %s' % req )
    for key in data.keys():
        if key not in good[table]['required'] and \
        key not in good[table]['optional']:
            raise Proauth2Error( 'invalid_request', 'invalid field: %s' % key )
    return good[table]['key']