def modelSetCompleted(self, modelID, completionReason, completionMsg,
                        cpuTime=0, useConnectionID=True):
    """ Mark a model as completed, with the given completionReason and
    completionMsg. This will fail if the model does not currently belong to this
    client (connection_id doesn't match).

    Parameters:
    ----------------------------------------------------------------
    modelID:             model ID of model to modify
    completionReason:    completionReason string
    completionMsg:       completionMsg string
    cpuTime:             amount of CPU time spent on this model
    useConnectionID:     True if the connection id of the calling function
                          must be the same as the connection that created the
                          job. Set to True for hypersearch workers, which use
                          this mechanism for orphaned model detection.
    """
    if completionMsg is None:
      completionMsg = ''

    query = 'UPDATE %s SET status=%%s, ' \
              '            completion_reason=%%s, ' \
              '            completion_msg=%%s, ' \
              '            end_time=UTC_TIMESTAMP(), ' \
              '            cpu_time=%%s, ' \
              '            _eng_last_update_time=UTC_TIMESTAMP(), ' \
              '            update_counter=update_counter+1 ' \
              '        WHERE model_id=%%s' \
              % (self.modelsTableName,)
    sqlParams = [self.STATUS_COMPLETED, completionReason, completionMsg,
                 cpuTime, modelID]

    if useConnectionID:
      query += " AND _eng_worker_conn_id=%s"
      sqlParams.append(self._connectionID)

    with ConnectionFactory.get() as conn:
      numRowsAffected = conn.cursor.execute(query, sqlParams)

    if numRowsAffected != 1:
      raise InvalidConnectionException(
        ("Tried to set modelID=%r using connectionID=%r, but this model "
         "belongs to some other worker or modelID not found; "
         "numRowsAffected=%r") % (modelID, self._connectionID, numRowsAffected))