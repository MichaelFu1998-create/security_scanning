def modelInsertAndStart(self, jobID, params, paramsHash, particleHash=None):
    """ Insert a new unique model (based on params) into the model table in the
    "running" state. This will return two things: whether or not the model was
    actually inserted (i.e. that set of params isn't already in the table) and
    the modelID chosen for that set of params. Even if the model was not
    inserted by this call (it was already there) the modelID of the one already
    inserted is returned.

    Parameters:
    ----------------------------------------------------------------
    jobID:            jobID of the job to add models for
    params:           params for this model
    paramsHash        hash of the params, generated by the worker
    particleHash      hash of the particle info (for PSO). If not provided,
                      then paramsHash will be used.

    retval:           (modelID, wasInserted)
                      modelID: the model ID for this set of params
                      wasInserted: True if this call ended up inserting the
                      new model. False if this set of params was already in
                      the model table.
    """
    # Fill in default particleHash
    if particleHash is None:
      particleHash = paramsHash

    # Normalize hashes
    paramsHash = self._normalizeHash(paramsHash)
    particleHash = self._normalizeHash(particleHash)

    def findExactMatchNoRetries(conn):
      return self._getOneMatchingRowNoRetries(
        self._models, conn,
        {'job_id':jobID, '_eng_params_hash':paramsHash,
         '_eng_particle_hash':particleHash},
        ['model_id', '_eng_worker_conn_id'])

    @g_retrySQL
    def findExactMatchWithRetries():
      with ConnectionFactory.get() as conn:
        return findExactMatchNoRetries(conn)

    # Check if the model is already in the models table
    #
    # NOTE: with retries of mysql transient failures, we can't always tell
    #  whether the row was already inserted (e.g., comms failure could occur
    #  after insertion into table, but before arrival or response), so the
    #  need to check before attempting to insert a new row
    #
    # TODO: if we could be assured that the caller already verified the
    #  model's absence before calling us, we could skip this check here
    row = findExactMatchWithRetries()
    if row is not None:
      return (row[0], False)

    @g_retrySQL
    def insertModelWithRetries():
      """ NOTE: it's possible that another process on some machine is attempting
      to insert the same model at the same time as the caller """
      with ConnectionFactory.get() as conn:
        # Create a new job entry
        query = 'INSERT INTO %s (job_id, params, status, _eng_params_hash, ' \
                '  _eng_particle_hash, start_time, _eng_last_update_time, ' \
                '  _eng_worker_conn_id) ' \
                '  VALUES (%%s, %%s, %%s, %%s, %%s, UTC_TIMESTAMP(), ' \
                '          UTC_TIMESTAMP(), %%s) ' \
                % (self.modelsTableName,)
        sqlParams = (jobID, params, self.STATUS_RUNNING, paramsHash,
                     particleHash, self._connectionID)
        try:
          numRowsAffected = conn.cursor.execute(query, sqlParams)
        except Exception, e:
          # NOTE: We have seen instances where some package in the calling
          #  chain tries to interpret the exception message using unicode.
          #  Since the exception message contains binary data (the hashes), this
          #  can in turn generate a Unicode translation exception. So, we catch
          #  ALL exceptions here and look for the string "Duplicate entry" in
          #  the exception args just in case this happens. For example, the
          #  Unicode exception we might get is:
          #   (<type 'exceptions.UnicodeDecodeError'>, UnicodeDecodeError('utf8', "Duplicate entry '1000-?.\x18\xb1\xd3\xe0CO\x05\x8b\xf80\xd7E5\xbb' for key 'job_id'", 25, 26, 'invalid start byte'))
          #
          #  If it weren't for this possible Unicode translation error, we
          #  could watch for only the exceptions we want, like this:
          #  except pymysql.IntegrityError, e:
          #    if e.args[0] != mysqlerrors.DUP_ENTRY:
          #      raise
          if "Duplicate entry" not in str(e):
            raise

          # NOTE: duplicate entry scenario: however, we can't discern
          # whether it was inserted by another process or this one, because an
          # intermittent failure may have caused us to retry
          self._logger.info('Model insert attempt failed with DUP_ENTRY: '
                            'jobID=%s; paramsHash=%s OR particleHash=%s; %r',
                            jobID, paramsHash.encode('hex'),
                            particleHash.encode('hex'), e)
        else:
          if numRowsAffected == 1:
            # NOTE: SELECT LAST_INSERT_ID() returns 0 after re-connection
            conn.cursor.execute('SELECT LAST_INSERT_ID()')
            modelID = conn.cursor.fetchall()[0][0]
            if modelID != 0:
              return (modelID, True)
            else:
              self._logger.warn(
                'SELECT LAST_INSERT_ID for model returned 0, implying loss of '
                'connection: jobID=%s; paramsHash=%r; particleHash=%r',
                jobID, paramsHash, particleHash)
          else:
            self._logger.error(
              'Attempt to insert model resulted in unexpected numRowsAffected: '
              'expected 1, but got %r; jobID=%s; paramsHash=%r; '
              'particleHash=%r',
              numRowsAffected, jobID, paramsHash, particleHash)

        # Look up the model and discern whether it is tagged with our conn id
        row = findExactMatchNoRetries(conn)
        if row is not None:
          (modelID, connectionID) = row
          return (modelID, connectionID == self._connectionID)

        # This set of params is already in the table, just get the modelID
        query = 'SELECT (model_id) FROM %s ' \
                '                  WHERE job_id=%%s AND ' \
                '                        (_eng_params_hash=%%s ' \
                '                         OR _eng_particle_hash=%%s) ' \
                '                  LIMIT 1 ' \
                % (self.modelsTableName,)
        sqlParams = [jobID, paramsHash, particleHash]
        numRowsFound = conn.cursor.execute(query, sqlParams)
        assert numRowsFound == 1, (
          'Model not found: jobID=%s AND (paramsHash=%r OR particleHash=%r); '
          'numRowsFound=%r') % (jobID, paramsHash, particleHash, numRowsFound)
        (modelID,) = conn.cursor.fetchall()[0]
        return (modelID, False)


    return insertModelWithRetries()