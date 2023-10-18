def _getExperimentDescriptionSchema():
  """
  Returns the experiment description schema. This implementation loads it in
  from file experimentDescriptionSchema.json.

  Parameters:
  --------------------------------------------------------------------------
  Returns:    returns a dict representing the experiment description schema.
  """
  installPath = os.path.dirname(os.path.abspath(__file__))
  schemaFilePath = os.path.join(installPath, "experimentDescriptionSchema.json")
  return json.loads(open(schemaFilePath, 'r').read())