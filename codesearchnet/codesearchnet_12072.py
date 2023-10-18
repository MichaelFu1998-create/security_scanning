def newcursor(self, dictcursor=False):
        '''
        This creates a DB cursor for the current DB connection using a
        randomly generated handle. Returns a tuple with cursor and handle.

        Parameters
        ----------

        dictcursor : bool
            If True, returns a cursor where each returned row can be addressed
            as a dictionary by column name.

        Returns
        -------

        tuple
            The tuple is of the form (handle, psycopg2.Cursor instance).

        '''

        handle = hashlib.sha256(os.urandom(12)).hexdigest()

        if dictcursor:
            self.cursors[handle] = self.connection.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            )
        else:
            self.cursors[handle] = self.connection.cursor()

            return (self.cursors[handle], handle)