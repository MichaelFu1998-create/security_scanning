def jobCancelAllRunningJobs(self):
    """ Set cancel field of all currently-running jobs to true.
    """

    # Get a database connection and cursor
    with ConnectionFactory.get() as conn:

      query = 'UPDATE %s SET cancel=TRUE WHERE status<>%%s ' \
              % (self.jobsTableName,)
      conn.cursor.execute(query, [self.STATUS_COMPLETED])

    return