def jobSetFieldIfEqual(self, jobID, fieldName, newValue, curValue):
    """ Change the value of 1 field in a job to 'newValue', but only if the
    current value matches 'curValue'. The 'fieldName' is the public name of
    the field (camelBack, not the lower_case_only form as stored in the DB).

    This method is used for example by HypersearcWorkers to update the
    engWorkerState field periodically. By qualifying on curValue, it insures
    that only 1 worker at a time is elected to perform the next scheduled
    periodic sweep of the models.

    Parameters:
    ----------------------------------------------------------------
    jobID:        jobID of the job record to modify
    fieldName:    public field name of the field
    newValue:     new value of the field to set
    curValue:     current value to qualify against

    retval:       True if we successfully modified the field
                  False if curValue did not match
    """

    # Get the private field name and string form of the value
    dbFieldName = self._jobs.pubToDBNameDict[fieldName]

    conditionValue = []
    if isinstance(curValue, bool):
      conditionExpression = '%s IS %s' % (
        dbFieldName, {True:'TRUE', False:'FALSE'}[curValue])
    elif curValue is None:
      conditionExpression = '%s is NULL' % (dbFieldName,)
    else:
      conditionExpression = '%s=%%s' % (dbFieldName,)
      conditionValue.append(curValue)

    query = 'UPDATE %s SET _eng_last_update_time=UTC_TIMESTAMP(), %s=%%s ' \
            '          WHERE job_id=%%s AND %s' \
            % (self.jobsTableName, dbFieldName, conditionExpression)
    sqlParams = [newValue, jobID] + conditionValue

    with ConnectionFactory.get() as conn:
      result = conn.cursor.execute(query, sqlParams)

    return (result == 1)