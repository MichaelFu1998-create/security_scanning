def validate(value, **kwds):
  """ Validate a python value against json schema:
  validate(value, schemaPath)
  validate(value, schemaDict)

  value:          python object to validate against the schema

  The json schema may be specified either as a path of the file containing
  the json schema or as a python dictionary using one of the
  following keywords as arguments:
    schemaPath:     Path of file containing the json schema object.
    schemaDict:     Python dictionary containing the json schema object

  Returns: nothing

  Raises:
          ValidationError when value fails json validation
  """

  assert len(kwds.keys()) >= 1
  assert 'schemaPath' in kwds or 'schemaDict' in kwds

  schemaDict = None
  if 'schemaPath' in kwds:
    schemaPath = kwds.pop('schemaPath')
    schemaDict = loadJsonValueFromFile(schemaPath)
  elif 'schemaDict' in kwds:
    schemaDict = kwds.pop('schemaDict')

  try:
    validictory.validate(value, schemaDict, **kwds)
  except validictory.ValidationError as e:
    raise ValidationError(e)