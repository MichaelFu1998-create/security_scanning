def getActiveJobCountForClientKey(self, clientKey):
    """ Return the number of jobs for the given clientKey and a status that is
    not completed.
    """
    with ConnectionFactory.get() as conn:
      query = 'SELECT count(job_id) ' \
              'FROM %s ' \
              'WHERE client_key = %%s ' \
              ' AND status != %%s' %  self.jobsTableName
      conn.cursor.execute(query, [clientKey, self.STATUS_COMPLETED])
      activeJobCount = conn.cursor.fetchone()[0]

    return activeJobCount