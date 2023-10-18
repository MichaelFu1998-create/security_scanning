def jobCountCancellingJobs(self,):
    """ Look through the jobs table and count the running jobs whose
    cancel field is true.

    Parameters:
    ----------------------------------------------------------------
    retval:      A count of running jobs with the cancel field set to true.
    """
    with ConnectionFactory.get() as conn:
      query = 'SELECT COUNT(job_id) '\
              'FROM %s ' \
              'WHERE (status<>%%s AND cancel is TRUE)' \
              % (self.jobsTableName,)

      conn.cursor.execute(query, [self.STATUS_COMPLETED])
      rows = conn.cursor.fetchall()

    return rows[0][0]