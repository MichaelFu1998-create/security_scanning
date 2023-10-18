def getActiveJobsForClientInfo(self, clientInfo, fields=[]):
    """ Fetch jobIDs for jobs in the table with optional fields given a
    specific clientInfo """

    # Form the sequence of field name strings that will go into the
    #  request
    dbFields = [self._jobs.pubToDBNameDict[x] for x in fields]
    dbFieldsStr = ','.join(['job_id'] + dbFields)

    with ConnectionFactory.get() as conn:
      query = 'SELECT %s FROM %s ' \
              'WHERE client_info = %%s ' \
              ' AND status != %%s' % (dbFieldsStr, self.jobsTableName)
      conn.cursor.execute(query, [clientInfo, self.STATUS_COMPLETED])
      rows = conn.cursor.fetchall()

    return rows