def store( self, collection, **kwargs ):
        '''
        validate the passed values in kwargs based on the collection,
        store them in the mongodb collection
        '''
        key = validate( collection, **kwargs )
        if self.fetch( collection, **{ key : kwargs[key] } ):
            raise Proauth2Error( 'duplicate_key' )
        self.db[collection].insert( kwargs )