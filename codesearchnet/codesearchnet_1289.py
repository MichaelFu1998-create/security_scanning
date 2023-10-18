def jobInfoWithModels(self, jobID):
    """ Get all info about a job, with model details, if available.

    Parameters:
    ----------------------------------------------------------------
    job:    jobID of the job to query
    retval: A sequence of two-tuples if the jobID exists in the jobs
             table (exeption is raised if it doesn't exist). Each two-tuple
             contains an instance of jobInfoNamedTuple as the first element and
             an instance of modelInfoNamedTuple as the second element. NOTE: In
             the case where there are no matching model rows, a sequence of one
             two-tuple will still be returned, but the modelInfoNamedTuple
             fields will be None, and the jobInfoNamedTuple fields will be
             populated.
    """

    # Get a database connection and cursor
    combinedResults = None

    with ConnectionFactory.get() as conn:
      # NOTE: Since we're using a LEFT JOIN on the models table, there need not
      # be a matching row in the models table, but the matching row from the
      # jobs table will still be returned (along with all fields from the models
      # table with values of None in case there were no matchings models)
      query = ' '.join([
        'SELECT %s.*, %s.*' % (self.jobsTableName, self.modelsTableName),
        'FROM %s' % self.jobsTableName,
        'LEFT JOIN %s USING(job_id)' % self.modelsTableName,
        'WHERE job_id=%s'])

      conn.cursor.execute(query, (jobID,))

      if conn.cursor.rowcount > 0:
        combinedResults = [
          ClientJobsDAO._combineResults(
            result, self._jobs.jobInfoNamedTuple,
            self._models.modelInfoNamedTuple
          ) for result in conn.cursor.fetchall()]

    if combinedResults is not None:
      return combinedResults

    raise RuntimeError("jobID=%s not found within the jobs table" % (jobID))