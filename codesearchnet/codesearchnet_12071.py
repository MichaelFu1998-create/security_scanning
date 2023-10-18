def cursor(self, handle, dictcursor=False):
        '''This gets or creates a DB cursor for the current DB connection.

        Parameters
        ----------

        handle : str
            The name of the cursor to look up in the existing list or if it
            doesn't exist, the name to be used for a new cursor to be returned.

        dictcursor : bool
            If True, returns a cursor where each returned row can be addressed
            as a dictionary by column name.

        Returns
        -------

        psycopg2.Cursor instance

        '''

        if handle in self.cursors:

            return self.cursors[handle]

        else:
            if dictcursor:
                self.cursors[handle] = self.connection.cursor(
                    cursor_factory=psycopg2.extras.DictCursor
                )
            else:
                self.cursors[handle] = self.connection.cursor()

            return self.cursors[handle]