def getFieldsForActiveJobsOfType(self, jobType, fields=[]):
    """ Helper function for querying the models table including relevant job
    info where the job type matches the specified jobType.  Only records for
    which there is a matching jobId in both tables is returned, and only the
    requested fields are returned in each result, assuming that there is not
    a conflict.  This function is useful, for example, in querying a cluster
    for a list of actively running production models (according to the state
    of the client jobs database).  jobType must be one of the JOB_TYPE_XXXX
    enumerations.

    Parameters:
    ----------------------------------------------------------------
    jobType:   jobType enum
    fields:    list of fields to return

    Returns:    List of tuples containing the jobId and requested field values
    """
    dbFields = [self._jobs.pubToDBNameDict[x] for x in fields]
    dbFieldsStr = ','.join(['job_id'] + dbFields)
    with ConnectionFactory.get() as conn:
      query = \
        'SELECT DISTINCT %s ' \
        'FROM %s j ' \
        'LEFT JOIN %s m USING(job_id) '\
        'WHERE j.status != %%s ' \
          'AND _eng_job_type = %%s' % (dbFieldsStr, self.jobsTableName,
            self.modelsTableName)

      conn.cursor.execute(query, [self.STATUS_COMPLETED, jobType])
      return conn.cursor.fetchall()