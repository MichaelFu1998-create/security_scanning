def jobReactivateRunningJobs(self):
    """ Look through the jobs table and reactivate all that are already in the
    running state by setting their _eng_allocate_new_workers fields to True;
    used by Nupic Scheduler as part of its failure-recovery procedure.
    """

    # Get a database connection and cursor
    with ConnectionFactory.get() as conn:

      query = 'UPDATE %s SET _eng_cjm_conn_id=%%s, ' \
              '              _eng_allocate_new_workers=TRUE ' \
              '    WHERE status=%%s ' \
              % (self.jobsTableName,)
      conn.cursor.execute(query, [self._connectionID, self.STATUS_RUNNING])

    return