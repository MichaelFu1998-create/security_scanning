def open(self, database, user, password, host):
        '''This opens a new database connection.

        Parameters
        ----------

        database : str
            Name of the database to connect to.

        user : str
            User name of the database server user.

        password : str
            Password for the database server user.

        host : str
            Database hostname or IP address to connect to.

        '''

        try:

            self.connection = pg.connect(user=user,
                                         password=password,
                                         database=database,
                                         host=host)

            LOGINFO('postgres connection successfully '
                    'created, using DB %s, user %s' % (database,
                                                       user))

            self.database = database
            self.user = user

        except Exception as e:

            LOGEXCEPTION('postgres connection failed, '
                         'using DB %s, user %s' % (database,
                                                   user))

            self.database = None
            self.user = None