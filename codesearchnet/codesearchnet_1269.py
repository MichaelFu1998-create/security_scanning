def connect(self, deleteOldVersions=False, recreate=False):
    """ Locate the current version of the jobs DB or create a new one, and
    optionally delete old versions laying around. If desired, this method
    can be called at any time to re-create the tables from scratch, delete
    old versions of the database, etc.

    Parameters:
    ----------------------------------------------------------------
    deleteOldVersions:   if true, delete any old versions of the DB left
                          on the server
    recreate:            if true, recreate the database from scratch even
                          if it already exists.
    """

    # Initialize tables, if needed
    with ConnectionFactory.get() as conn:
      # Initialize tables
      self._initTables(cursor=conn.cursor, deleteOldVersions=deleteOldVersions,
                       recreate=recreate)

      # Save our connection id
      conn.cursor.execute('SELECT CONNECTION_ID()')
      self._connectionID = conn.cursor.fetchall()[0][0]
      self._logger.info("clientJobsConnectionID=%r", self._connectionID)

    return