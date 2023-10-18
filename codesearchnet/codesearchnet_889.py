def _handleModelRunnerException(jobID, modelID, jobsDAO, experimentDir, logger,
                                e):
  """ Perform standard handling of an exception that occurs while running
  a model.

  Parameters:
  -------------------------------------------------------------------------
  jobID:                ID for this hypersearch job in the jobs table
  modelID:              model ID
  jobsDAO:              ClientJobsDAO instance
  experimentDir:        directory containing the experiment
  logger:               the logger to use
  e:                    the exception that occurred
  retval:               (completionReason, completionMsg)
  """

  msg = StringIO.StringIO()
  print >>msg, "Exception occurred while running model %s: %r (%s)" % (
    modelID, e, type(e))
  traceback.print_exc(None, msg)

  completionReason = jobsDAO.CMPL_REASON_ERROR
  completionMsg = msg.getvalue()
  logger.error(completionMsg)

  # Write results to the model database for the error case. Ignore
  # InvalidConnectionException, as this is usually caused by orphaned models
  #
  # TODO: do we really want to set numRecords to 0? Last updated value might
  #       be useful for debugging
  if type(e) is not InvalidConnectionException:
    jobsDAO.modelUpdateResults(modelID,  results=None, numRecords=0)

  # TODO: Make sure this wasn't the best model in job. If so, set the best
  # appropriately

  # If this was an exception that should mark the job as failed, do that
  # now.
  if type(e) == JobFailException:
    workerCmpReason = jobsDAO.jobGetFields(jobID,
        ['workerCompletionReason'])[0]
    if workerCmpReason == ClientJobsDAO.CMPL_REASON_SUCCESS:
      jobsDAO.jobSetFields(jobID, fields=dict(
          cancel=True,
          workerCompletionReason = ClientJobsDAO.CMPL_REASON_ERROR,
          workerCompletionMsg = ": ".join(str(i) for i in e.args)),
          useConnectionID=False,
          ignoreUnchanged=True)

  return (completionReason, completionMsg)