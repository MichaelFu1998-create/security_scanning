def modelsGetFieldsForJob(self, jobID, fields, ignoreKilled=False):
    """ Gets the specified fields for all the models for a single job. This is
    similar to modelsGetFields

    Parameters:
    ----------------------------------------------------------------
    jobID:              jobID for the models to be searched
    fields:             A list  of fields to return
    ignoreKilled:       (True/False). If True, this will ignore models that
                        have been killed

    Returns: a (possibly empty) list of tuples as follows
      [
        (model_id1, [field1, ..., fieldn]),
        (model_id2, [field1, ..., fieldn]),
        (model_id3, [field1, ..., fieldn])
                    ...
      ]

    NOTE: since there is a window of time between a job getting inserted into
     jobs table and the job's worker(s) starting up and creating models, an
     empty-list result is one of the normal outcomes.
    """

    assert len(fields) >= 1, 'fields is empty'

    # Form the sequence of field name strings that will go into the
    #  request
    dbFields = [self._models.pubToDBNameDict[x] for x in fields]
    dbFieldsStr = ','.join(dbFields)

    query = 'SELECT model_id, %s FROM %s ' \
              '          WHERE job_id=%%s ' \
              % (dbFieldsStr, self.modelsTableName)
    sqlParams = [jobID]

    if ignoreKilled:
      query += ' AND (completion_reason IS NULL OR completion_reason != %s)'
      sqlParams.append(self.CMPL_REASON_KILLED)

    # Get a database connection and cursor
    with ConnectionFactory.get() as conn:
      conn.cursor.execute(query, sqlParams)
      rows = conn.cursor.fetchall()

    if rows is None:
      # fetchall is defined to return a (possibly-empty) sequence of
      # sequences; however, we occasionally see None returned and don't know
      # why...
      self._logger.error("Unexpected None result from cursor.fetchall; "
                         "query=%r; Traceback=%r",
                         query, traceback.format_exc())

    return [(r[0], list(r[1:])) for r in rows]