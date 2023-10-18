def jobUpdateResults(self, jobID, results):
    """ Update the results string and last-update-time fields of a model.

    Parameters:
    ----------------------------------------------------------------
    jobID:      job ID of model to modify
    results:    new results (json dict string)
    """
    with ConnectionFactory.get() as conn:
      query = 'UPDATE %s SET _eng_last_update_time=UTC_TIMESTAMP(), ' \
              '              results=%%s ' \
              '          WHERE job_id=%%s' % (self.jobsTableName,)
      conn.cursor.execute(query, [results, jobID])