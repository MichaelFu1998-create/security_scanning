def _initTables(self, cursor, deleteOldVersions, recreate):
    """ Initialize tables, if needed

    Parameters:
    ----------------------------------------------------------------
    cursor:              SQL cursor
    deleteOldVersions:   if true, delete any old versions of the DB left
                          on the server
    recreate:            if true, recreate the database from scratch even
                          if it already exists.
    """

    # Delete old versions if they exist
    if deleteOldVersions:
      self._logger.info(
        "Dropping old versions of client_jobs DB; called from: %r",
        traceback.format_stack())
      for i in range(self._DB_VERSION):
        cursor.execute('DROP DATABASE IF EXISTS %s' %
                              (self.__getDBNameForVersion(i),))

    # Create the database if necessary
    if recreate:
      self._logger.info(
        "Dropping client_jobs DB %r; called from: %r",
        self.dbName, traceback.format_stack())
      cursor.execute('DROP DATABASE IF EXISTS %s' % (self.dbName))

    cursor.execute('CREATE DATABASE IF NOT EXISTS %s' % (self.dbName))


    # Get the list of tables
    cursor.execute('SHOW TABLES IN %s' % (self.dbName))
    output = cursor.fetchall()
    tableNames = [x[0] for x in output]

    # ------------------------------------------------------------------------
    # Create the jobs table if it doesn't exist
    # Fields that start with '_eng' are intended for private use by the engine
    #  and should not be used by the UI
    if 'jobs' not in tableNames:
      self._logger.info("Creating table %r", self.jobsTableName)
      fields = [
        'job_id                  INT UNSIGNED NOT NULL AUTO_INCREMENT',
            # unique jobID
        'client                  CHAR(%d)' % (self.CLIENT_MAX_LEN),
            # name of client (UI, StrmMgr, etc.)
        'client_info             LONGTEXT',
            # Arbitrary data defined by the client
        'client_key             varchar(255)',
            # Foreign key as defined by the client.
        'cmd_line                LONGTEXT',
            # command line to use to launch each worker process
        'params                  LONGTEXT',
            # JSON encoded params for the job, for use by the worker processes
        'job_hash                BINARY(%d) DEFAULT NULL' % (self.HASH_MAX_LEN),
            # unique hash of the job, provided by the client. Used for detecting
            # identical job requests from the same client when they use the
            # jobInsertUnique() method.
        'status                  VARCHAR(16) DEFAULT "notStarted"',
            # One of the STATUS_XXX enumerated value strings
        'completion_reason       VARCHAR(16)',
            # One of the CMPL_REASON_XXX enumerated value strings.
            # NOTE: This is the job completion reason according to the hadoop
            # job-tracker. A success here does not necessarily mean the
            # workers were "happy" with the job. To see if the workers
            # failed, check the worker_completion_reason
        'completion_msg          LONGTEXT',
            # Why this job completed, according to job-tracker
        'worker_completion_reason   VARCHAR(16) DEFAULT "%s"'  % \
                  self.CMPL_REASON_SUCCESS,
            # One of the CMPL_REASON_XXX enumerated value strings. This is
            # may be changed to CMPL_REASON_ERROR if any workers encounter
            # an error while running the job.
        'worker_completion_msg   LONGTEXT',
            # Why this job completed, according to workers. If
            # worker_completion_reason is set to CMPL_REASON_ERROR, this will
            # contain the error information.
        'cancel                  BOOLEAN DEFAULT FALSE',
            # set by UI, polled by engine
        'start_time              DATETIME DEFAULT NULL',
            # When job started
        'end_time                DATETIME DEFAULT NULL',
            # When job ended
        'results                 LONGTEXT',
            # JSON dict with general information about the results of the job,
            # including the ID and value of the best model
            # TODO: different semantics for results field of ProductionJob
        '_eng_job_type           VARCHAR(32)',
            # String used to specify the type of job that this is. Current
            # choices are hypersearch, production worker, or stream worker
        'minimum_workers         INT UNSIGNED DEFAULT 0',
            # min number of desired workers at a time. If 0, no workers will be
            # allocated in a crunch
        'maximum_workers         INT UNSIGNED DEFAULT 0',
            # max number of desired workers at a time. If 0, then use as many
            # as practical given load on the cluster.
        'priority                 INT DEFAULT %d' % self.DEFAULT_JOB_PRIORITY,
            # job scheduling priority; 0 is the default priority (
            # ClientJobsDAO.DEFAULT_JOB_PRIORITY); positive values are higher
            # priority (up to ClientJobsDAO.MAX_JOB_PRIORITY), and negative
            # values are lower priority (down to ClientJobsDAO.MIN_JOB_PRIORITY)
        '_eng_allocate_new_workers    BOOLEAN DEFAULT TRUE',
            # Should the scheduling algorithm allocate new workers to this job?
            # If a specialized worker willingly gives up control, we set this
            # field to FALSE to avoid allocating new workers.
        '_eng_untended_dead_workers   BOOLEAN DEFAULT FALSE',
            # If a specialized worker fails or is killed by the scheduler, we
            # set this feild to TRUE to indicate that the worker is dead
        'num_failed_workers           INT UNSIGNED DEFAULT 0',
            # The number of failed specialized workers for this job. If the
            # number of failures is >= max.failed.attempts, we mark the job
            # as failed
        'last_failed_worker_error_msg  LONGTEXT',
            # Error message of the most recent specialized failed worker
        '_eng_cleaning_status          VARCHAR(16) DEFAULT "%s"'  % \
                  self.CLEAN_NOT_DONE,
            # Has the job been garbage collected, this includes removing
            # unneeded # model output caches, s3 checkpoints.
        'gen_base_description    LONGTEXT',
            # The contents of the generated description.py file from hypersearch
            # requests. This is generated by the Hypersearch workers and stored
            # here for reference, debugging, and development purposes.
        'gen_permutations        LONGTEXT',
            # The contents of the generated permutations.py file from
            # hypersearch requests. This is generated by the Hypersearch workers
            # and stored here for reference, debugging, and development
            # purposes.
        '_eng_last_update_time   DATETIME DEFAULT NULL',
            # time stamp of last update, used for detecting stalled jobs
        '_eng_cjm_conn_id        INT UNSIGNED',
            # ID of the CJM starting up this job
        '_eng_worker_state       LONGTEXT',
            # JSON encoded state of the hypersearch in progress, for private
            # use by the Hypersearch workers
        '_eng_status             LONGTEXT',
            # String used for status messages sent from the engine for
            # informative purposes only. Usually printed periodically by
            # clients watching a job progress.
        '_eng_model_milestones   LONGTEXT',
            # JSon encoded object with information about global model milestone
            # results

        'PRIMARY KEY (job_id)',
        'UNIQUE INDEX (client, job_hash)',
        'INDEX (status)',
        'INDEX (client_key)'
        ]
      options = [
        'AUTO_INCREMENT=1000',
        ]

      query = 'CREATE TABLE IF NOT EXISTS %s (%s) %s' % \
                (self.jobsTableName, ','.join(fields), ','.join(options))

      cursor.execute(query)


    # ------------------------------------------------------------------------
    # Create the models table if it doesn't exist
    # Fields that start with '_eng' are intended for private use by the engine
    #  and should not be used by the UI
    if 'models' not in tableNames:
      self._logger.info("Creating table %r", self.modelsTableName)
      fields = [
        'model_id                BIGINT UNSIGNED NOT NULL AUTO_INCREMENT',
            # globally unique model ID
        'job_id                  INT UNSIGNED NOT NULL',
            # jobID
        'params                  LONGTEXT NOT NULL',
            # JSON encoded params for the model
        'status                  VARCHAR(16) DEFAULT "notStarted"',
            # One of the STATUS_XXX enumerated value strings
        'completion_reason       VARCHAR(16)',
            # One of the CMPL_REASON_XXX enumerated value strings
        'completion_msg          LONGTEXT',
            # Why this job completed
        'results                 LONGTEXT DEFAULT NULL',
            # JSON encoded structure containing metrics produced by the model
        'optimized_metric        FLOAT ',
            #Value of the particular metric we are optimizing in hypersearch
        'update_counter          INT UNSIGNED DEFAULT 0',
            # incremented by engine every time the results is updated
        'num_records             INT UNSIGNED DEFAULT 0',
            # number of records processed so far
        'start_time              DATETIME DEFAULT NULL',
            # When this model started being evaluated
        'end_time                DATETIME DEFAULT NULL',
            # When this model completed
        'cpu_time                FLOAT DEFAULT 0',
            # How much actual CPU time was spent on this model, in seconds. This
            #  excludes time the process spent sleeping, or otherwise not
            #  actually executing code.
        'model_checkpoint_id     LONGTEXT',
            # Checkpoint identifier for this model (after it has been saved)
        'gen_description         LONGTEXT',
            # The contents of the generated description.py file from hypersearch
            # requests. This is generated by the Hypersearch workers and stored
            # here for reference, debugging, and development purposes.
        '_eng_params_hash        BINARY(%d) DEFAULT NULL' % (self.HASH_MAX_LEN),
            # MD5 hash of the params
        '_eng_particle_hash      BINARY(%d) DEFAULT NULL' % (self.HASH_MAX_LEN),
            # MD5 hash of the particle info for PSO algorithm
        '_eng_last_update_time   DATETIME DEFAULT NULL',
            # time stamp of last update, used for detecting stalled workers
        '_eng_task_tracker_id    TINYBLOB',
            # Hadoop Task Tracker ID
        '_eng_worker_id          TINYBLOB',
            # Hadoop Map Task ID
        '_eng_attempt_id         TINYBLOB',
            # Hadoop Map task attempt ID
        '_eng_worker_conn_id     INT DEFAULT 0',
            # database client connection ID of the worker that is running this
            # model
        '_eng_milestones         LONGTEXT',
            # A JSON encoded list of metric values for the model at each
            #  milestone point
        '_eng_stop               VARCHAR(16) DEFAULT NULL',
            # One of the STOP_REASON_XXX enumerated value strings. Set either by
            # the swarm terminator of either the current, or another
            # Hypersearch worker.
        '_eng_matured            BOOLEAN DEFAULT FALSE',
            # Set by the model maturity-checker when it decides that this model
            #  has "matured". This means that it has reached the point of
            #  not getting better results with more data.
        'PRIMARY KEY (model_id)',
        'UNIQUE INDEX (job_id, _eng_params_hash)',
        'UNIQUE INDEX (job_id, _eng_particle_hash)',
        ]
      options = [
        'AUTO_INCREMENT=1000',
        ]

      query = 'CREATE TABLE IF NOT EXISTS %s (%s) %s' % \
              (self.modelsTableName, ','.join(fields), ','.join(options))

      cursor.execute(query)


    # ---------------------------------------------------------------------
    # Get the field names for each table
    cursor.execute('DESCRIBE %s' % (self.jobsTableName))
    fields = cursor.fetchall()
    self._jobs.dbFieldNames = [str(field[0]) for field in fields]

    cursor.execute('DESCRIBE %s' % (self.modelsTableName))
    fields = cursor.fetchall()
    self._models.dbFieldNames = [str(field[0]) for field in fields]


    # ---------------------------------------------------------------------
    # Generate the public names
    self._jobs.publicFieldNames = [self._columnNameDBToPublic(x)
                                   for x in self._jobs.dbFieldNames]
    self._models.publicFieldNames = [self._columnNameDBToPublic(x)
                                     for x in self._models.dbFieldNames]


    # ---------------------------------------------------------------------
    # Generate the name conversion dicts
    self._jobs.pubToDBNameDict = dict(
      zip(self._jobs.publicFieldNames, self._jobs.dbFieldNames))
    self._jobs.dbToPubNameDict = dict(
      zip(self._jobs.dbFieldNames, self._jobs.publicFieldNames))
    self._models.pubToDBNameDict = dict(
      zip(self._models.publicFieldNames, self._models.dbFieldNames))
    self._models.dbToPubNameDict = dict(
      zip(self._models.dbFieldNames, self._models.publicFieldNames))


    # ---------------------------------------------------------------------
    # Generate the dynamic namedtuple classes we use
    self._models.modelInfoNamedTuple = collections.namedtuple(
      '_modelInfoNamedTuple', self._models.publicFieldNames)

    self._jobs.jobInfoNamedTuple = collections.namedtuple(
      '_jobInfoNamedTuple', self._jobs.publicFieldNames)

    return