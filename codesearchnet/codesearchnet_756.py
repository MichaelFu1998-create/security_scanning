def createAndStartSwarm(client, clientInfo="", clientKey="", params="",
                        minimumWorkers=None, maximumWorkers=None,
                        alreadyRunning=False):
  """Create and start a swarm job.

  Args:
    client - A string identifying the calling client. There is a small limit
        for the length of the value. See ClientJobsDAO.CLIENT_MAX_LEN.
    clientInfo - JSON encoded dict of client specific information.
    clientKey - Foreign key. Limited in length, see ClientJobsDAO._initTables.
    params - JSON encoded dict of the parameters for the job. This can be
        fetched out of the database by the worker processes based on the jobID.
    minimumWorkers - The minimum workers to allocate to the swarm. Set to None
        to use the default.
    maximumWorkers - The maximum workers to allocate to the swarm. Set to None
        to use the swarm default. Set to 0 to use the maximum scheduler value.
    alreadyRunning - Insert a job record for an already running process. Used
        for testing.
  """
  if minimumWorkers is None:
    minimumWorkers = Configuration.getInt(
        "nupic.hypersearch.minWorkersPerSwarm")
  if maximumWorkers is None:
    maximumWorkers = Configuration.getInt(
        "nupic.hypersearch.maxWorkersPerSwarm")

  return ClientJobsDAO.get().jobInsert(
      client=client,
      cmdLine="$HYPERSEARCH",
      clientInfo=clientInfo,
      clientKey=clientKey,
      alreadyRunning=alreadyRunning,
      params=params,
      minimumWorkers=minimumWorkers,
      maximumWorkers=maximumWorkers,
      jobType=ClientJobsDAO.JOB_TYPE_HS)