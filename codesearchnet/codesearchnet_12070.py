def autocommit(self):
        '''
        This sets the database connection to autocommit. Must be called before
        any cursors have been instantiated.

        '''

        if len(self.cursors.keys()) == 0:
            self.connection.autocommit = True
        else:
            raise AttributeError('database cursors are already active, '
                                 'cannot switch to autocommit now')