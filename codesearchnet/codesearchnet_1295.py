def getActiveJobCountForClientInfo(self, clientInfo):
    """ Return the number of jobs for the given clientInfo and a status that is
    not completed.
    """
    with ConnectionFactory.get() as conn:
      query = 'SELECT count(job_id) ' \
              'FROM %s ' \
              'WHERE client_info = %%s ' \
              ' AND status != %%s' %  self.jobsTableName
      conn.cursor.execute(query, [clientInfo, self.STATUS_COMPLETED])
      activeJobCount = conn.cursor.fetchone()[0]

    return activeJobCount