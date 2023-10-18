def jobGetCancellingJobs(self,):
    """ Look through the jobs table and get the list of running jobs whose
    cancel field is true.

    Parameters:
    ----------------------------------------------------------------
    retval:      A (possibly empty) sequence of running job IDs with cancel field
                  set to true
    """
    with ConnectionFactory.get() as conn:
      query = 'SELECT job_id '\
              'FROM %s ' \
              'WHERE (status<>%%s AND cancel is TRUE)' \
              % (self.jobsTableName,)
      conn.cursor.execute(query, [self.STATUS_COMPLETED])
      rows = conn.cursor.fetchall()

    return tuple(r[0] for r in rows)