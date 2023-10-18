def validateOpfJsonValue(value, opfJsonSchemaFilename):
  """
  Validate a python object against an OPF json schema file

  :param value: target python object to validate (typically a dictionary)
  :param opfJsonSchemaFilename: (string) OPF json schema filename containing the
         json schema object. (e.g., opfTaskControlSchema.json)
  :raises: jsonhelpers.ValidationError when value fails json validation
  """

  # Create a path by joining the filename with our local json schema root
  jsonSchemaPath = os.path.join(os.path.dirname(__file__),
                                "jsonschema",
                                opfJsonSchemaFilename)

  # Validate
  jsonhelpers.validate(value, schemaPath=jsonSchemaPath)

  return