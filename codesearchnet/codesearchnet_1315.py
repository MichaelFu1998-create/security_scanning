def modelUpdateResults(self, modelID, results=None, metricValue =None,
                         numRecords=None):
    """ Update the results string, and/or num_records fields of
    a model. This will fail if the model does not currently belong to this
    client (connection_id doesn't match).

    Parameters:
    ----------------------------------------------------------------
    modelID:      model ID of model to modify
    results:      new results, or None to ignore
    metricValue:  the value of the metric being optimized, or None to ignore
    numRecords:   new numRecords, or None to ignore
    """

    assignmentExpressions = ['_eng_last_update_time=UTC_TIMESTAMP()',
                             'update_counter=update_counter+1']
    assignmentValues = []

    if results is not None:
      assignmentExpressions.append('results=%s')
      assignmentValues.append(results)

    if numRecords is not None:
      assignmentExpressions.append('num_records=%s')
      assignmentValues.append(numRecords)

    # NOTE1: (metricValue==metricValue) tests for Nan
    # NOTE2: metricValue is being passed as numpy.float64
    if metricValue is not None and (metricValue==metricValue):
      assignmentExpressions.append('optimized_metric=%s')
      assignmentValues.append(float(metricValue))

    query = 'UPDATE %s SET %s ' \
            '          WHERE model_id=%%s and _eng_worker_conn_id=%%s' \
                % (self.modelsTableName, ','.join(assignmentExpressions))
    sqlParams = assignmentValues + [modelID, self._connectionID]

    # Get a database connection and cursor
    with ConnectionFactory.get() as conn:
      numRowsAffected = conn.cursor.execute(query, sqlParams)

    if numRowsAffected != 1:
      raise InvalidConnectionException(
        ("Tried to update the info of modelID=%r using connectionID=%r, but "
         "this model belongs to some other worker or modelID not found; "
         "numRowsAffected=%r") % (modelID,self._connectionID, numRowsAffected,))