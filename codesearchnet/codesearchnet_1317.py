def modelAdoptNextOrphan(self, jobId, maxUpdateInterval):
    """ Look through the models table for an orphaned model, which is a model
    that is not completed yet, whose _eng_last_update_time is more than
    maxUpdateInterval seconds ago.

    If one is found, change its _eng_worker_conn_id to the current worker's
    and return the model id.

    Parameters:
    ----------------------------------------------------------------
    retval:    modelId of the model we adopted, or None if none found
    """

    @g_retrySQL
    def findCandidateModelWithRetries():
      modelID = None
      with ConnectionFactory.get() as conn:
        # TODO: may need a table index on job_id/status for speed
        query = 'SELECT model_id FROM %s ' \
                '   WHERE  status=%%s ' \
                '          AND job_id=%%s ' \
                '          AND TIMESTAMPDIFF(SECOND, ' \
                '                            _eng_last_update_time, ' \
                '                            UTC_TIMESTAMP()) > %%s ' \
                '   LIMIT 1 ' \
                % (self.modelsTableName,)
        sqlParams = [self.STATUS_RUNNING, jobId, maxUpdateInterval]
        numRows = conn.cursor.execute(query, sqlParams)
        rows = conn.cursor.fetchall()

      assert numRows <= 1, "Unexpected numRows: %r" % numRows
      if numRows == 1:
        (modelID,) = rows[0]

      return modelID

    @g_retrySQL
    def adoptModelWithRetries(modelID):
      adopted = False
      with ConnectionFactory.get() as conn:
        query = 'UPDATE %s SET _eng_worker_conn_id=%%s, ' \
                  '            _eng_last_update_time=UTC_TIMESTAMP() ' \
                  '        WHERE model_id=%%s ' \
                  '              AND status=%%s' \
                  '              AND TIMESTAMPDIFF(SECOND, ' \
                  '                                _eng_last_update_time, ' \
                  '                                UTC_TIMESTAMP()) > %%s ' \
                  '        LIMIT 1 ' \
                  % (self.modelsTableName,)
        sqlParams = [self._connectionID, modelID, self.STATUS_RUNNING,
                     maxUpdateInterval]
        numRowsAffected = conn.cursor.execute(query, sqlParams)

        assert numRowsAffected <= 1, 'Unexpected numRowsAffected=%r' % (
          numRowsAffected,)

        if numRowsAffected == 1:
          adopted = True
        else:
          # Discern between transient failure during update and someone else
          # claiming this model
          (status, connectionID) = self._getOneMatchingRowNoRetries(
            self._models, conn, {'model_id':modelID},
            ['status', '_eng_worker_conn_id'])
          adopted = (status == self.STATUS_RUNNING and
                     connectionID == self._connectionID)
      return adopted


    adoptedModelID = None
    while True:
      modelID = findCandidateModelWithRetries()
      if modelID is None:
        break
      if adoptModelWithRetries(modelID):
        adoptedModelID = modelID
        break

    return adoptedModelID