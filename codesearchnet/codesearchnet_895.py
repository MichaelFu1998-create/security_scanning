def loadJsonValueFromFile(inputFilePath):
  """ Loads a json value from a file and converts it to the corresponding python
  object.

  inputFilePath:
                  Path of the json file;

  Returns:
                  python value that represents the loaded json value

  """
  with open(inputFilePath) as fileObj:
    value = json.load(fileObj)

  return value