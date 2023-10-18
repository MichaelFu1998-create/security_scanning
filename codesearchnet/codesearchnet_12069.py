def open_default(self):
        '''
        This opens the database connection using the default database parameters
        given in the ~/.astrobase/astrobase.conf file.

        '''

        if HAVECONF:
            self.open(DBDATA, DBUSER, DBPASS, DBHOST)
        else:
            LOGERROR("no default DB connection config found in lcdb.conf, "
                     "this function won't work otherwise")