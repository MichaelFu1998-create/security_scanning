def main(argv):
  """
  The main function of the HypersearchWorker script. This parses the command
  line arguments, instantiates a HypersearchWorker instance, and then
  runs it.

  Parameters:
  ----------------------------------------------------------------------
  retval:     jobID of the job we ran. This is used by unit test code
                when calling this working using the --params command
                line option (which tells this worker to insert the job
                itself).
  """

  parser = OptionParser(helpString)

  parser.add_option("--jobID", action="store", type="int", default=None,
        help="jobID of the job within the dbTable [default: %default].")

  parser.add_option("--modelID", action="store", type="str", default=None,
        help=("Tell worker to re-run this model ID. When specified, jobID "
         "must also be specified [default: %default]."))

  parser.add_option("--workerID", action="store", type="str", default=None,
        help=("workerID of the scheduler's SlotAgent (GenericWorker) that "
          "hosts this SpecializedWorker [default: %default]."))

  parser.add_option("--params", action="store", default=None,
        help="Create and execute a new hypersearch request using this JSON " \
        "format params string. This is helpful for unit tests and debugging. " \
        "When specified jobID must NOT be specified. [default: %default].")

  parser.add_option("--clearModels", action="store_true", default=False,
        help="clear out the models table before starting [default: %default].")

  parser.add_option("--resetJobStatus", action="store_true", default=False,
        help="Reset the job status before starting  [default: %default].")

  parser.add_option("--logLevel", action="store", type="int", default=None,
        help="override default log level. Pass in an integer value that "
        "represents the desired logging level (10=logging.DEBUG, "
        "20=logging.INFO, etc.) [default: %default].")

  # Evaluate command line arguments
  (options, args) = parser.parse_args(argv[1:])
  if len(args) != 0:
    raise RuntimeError("Expected no command line arguments, but got: %s" % \
                        (args))

  if (options.jobID and options.params):
    raise RuntimeError("--jobID and --params can not be used at the same time")

  if (options.jobID is None and options.params is None):
    raise RuntimeError("Either --jobID or --params must be specified.")

  initLogging(verbose=True)

  # Instantiate the HypersearchWorker and run it
  hst = HypersearchWorker(options, argv[1:])

  # Normal use. This is one of among a number of workers. If we encounter
  #  an exception at the outer loop here, we fail the entire job.
  if options.params is None:
    try:
      jobID = hst.run()

    except Exception, e:
      jobID = options.jobID
      msg = StringIO.StringIO()
      print >>msg, "%s: Exception occurred in Hypersearch Worker: %r" % \
         (ErrorCodes.hypersearchLogicErr, e)
      traceback.print_exc(None, msg)

      completionReason = ClientJobsDAO.CMPL_REASON_ERROR
      completionMsg = msg.getvalue()
      hst.logger.error(completionMsg)

      # If no other worker already marked the job as failed, do so now.
      jobsDAO = ClientJobsDAO.get()
      workerCmpReason = jobsDAO.jobGetFields(options.jobID,
          ['workerCompletionReason'])[0]
      if workerCmpReason == ClientJobsDAO.CMPL_REASON_SUCCESS:
        jobsDAO.jobSetFields(options.jobID, fields=dict(
            cancel=True,
            workerCompletionReason = ClientJobsDAO.CMPL_REASON_ERROR,
            workerCompletionMsg = completionMsg),
            useConnectionID=False,
            ignoreUnchanged=True)


  # Run just 1 worker for the entire job. Used for unit tests that run in
  # 1 process
  else:
    jobID = None
    completionReason = ClientJobsDAO.CMPL_REASON_SUCCESS
    completionMsg = "Success"

    try:
      jobID = hst.run()
    except Exception, e:
      jobID = hst._options.jobID
      completionReason = ClientJobsDAO.CMPL_REASON_ERROR
      completionMsg = "ERROR: %s" % (e,)
      raise
    finally:
      if jobID is not None:
        cjDAO = ClientJobsDAO.get()
        cjDAO.jobSetCompleted(jobID=jobID,
                              completionReason=completionReason,
                              completionMsg=completionMsg)

  return jobID