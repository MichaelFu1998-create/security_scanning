def rollback(self):
        '''
        This just calls the connection's commit method.

        '''
        if not self.connection.closed:
            self.connection.rollback()
        else:
            raise AttributeError('postgres connection to %s is closed' %
                                 self.database)