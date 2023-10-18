def modelSetFields(self, modelID, fields, ignoreUnchanged = False):
    """ Change the values of 1 or more fields in a model. Here, 'fields' is a
    dict with the name/value pairs to change. The names are the public names of
    the fields (camelBack, not the lower_case_only form as stored in the DB).

    Parameters:
    ----------------------------------------------------------------
    jobID:     jobID of the job record

    fields:    dictionary of fields to change

    ignoreUnchanged: The default behavior is to throw a
    RuntimeError if no rows are affected. This could either be
    because:
      1) Because there was no matching modelID
      2) or if the data to update matched the data in the DB exactly.

    Set this parameter to True if you expect case 2 and wish to
    supress the error.
    """

    # Form the sequence of key=value strings that will go into the
    #  request
    assignmentExpressions = ','.join(
      '%s=%%s' % (self._models.pubToDBNameDict[f],) for f in fields.iterkeys())
    assignmentValues = fields.values()

    query = 'UPDATE %s SET %s, update_counter = update_counter+1 ' \
            '          WHERE model_id=%%s' \
            % (self.modelsTableName, assignmentExpressions)
    sqlParams = assignmentValues + [modelID]

    # Get a database connection and cursor
    with ConnectionFactory.get() as conn:
      numAffectedRows = conn.cursor.execute(query, sqlParams)
      self._logger.debug("Executed: numAffectedRows=%r, query=%r, sqlParams=%r",
                         numAffectedRows, query, sqlParams)

    if numAffectedRows != 1 and not ignoreUnchanged:
      raise RuntimeError(
        ("Tried to change fields (%r) of model %r (conn_id=%r), but an error "
         "occurred. numAffectedRows=%r; query=%r; sqlParams=%r") % (
          fields, modelID, self._connectionID, numAffectedRows, query,
          sqlParams,))