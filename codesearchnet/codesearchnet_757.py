def getSwarmModelParams(modelID):
  """Retrieve the Engine-level model params from a Swarm model

  Args:
    modelID - Engine-level model ID of the Swarm model

  Returns:
    JSON-encoded string containing Model Params
  """

  # TODO: the use of nupic.frameworks.opf.helpers.loadExperimentDescriptionScriptFromDir when
  #  retrieving module params results in a leakage of pf_base_descriptionNN and
  #  pf_descriptionNN module imports for every call to getSwarmModelParams, so
  #  the leakage is unlimited when getSwarmModelParams is called by a
  #  long-running process.  An alternate solution is to execute the guts of
  #  this function's logic in a seprate process (via multiprocessing module).

  cjDAO = ClientJobsDAO.get()

  (jobID, description) = cjDAO.modelsGetFields(
    modelID,
    ["jobId", "genDescription"])

  (baseDescription,) = cjDAO.jobGetFields(jobID, ["genBaseDescription"])

  # Construct a directory with base.py and description.py for loading model
  # params, and use nupic.frameworks.opf.helpers to extract model params from
  # those files
  descriptionDirectory = tempfile.mkdtemp()
  try:
    baseDescriptionFilePath = os.path.join(descriptionDirectory, "base.py")
    with open(baseDescriptionFilePath, mode="wb") as f:
      f.write(baseDescription)

    descriptionFilePath = os.path.join(descriptionDirectory, "description.py")
    with open(descriptionFilePath, mode="wb") as f:
      f.write(description)

    expIface = helpers.getExperimentDescriptionInterfaceFromModule(
      helpers.loadExperimentDescriptionScriptFromDir(descriptionDirectory))

    return json.dumps(
      dict(
        modelConfig=expIface.getModelDescription(),
        inferenceArgs=expIface.getModelControl().get("inferenceArgs", None)))
  finally:
    shutil.rmtree(descriptionDirectory, ignore_errors=True)