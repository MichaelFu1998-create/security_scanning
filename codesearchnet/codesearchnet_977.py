def _getPropertyValue(schema, propertyName, options):
  """Checks to see if property is specified in 'options'. If not, reads the
  default value from the schema"""

  if propertyName not in options:
    paramsSchema = schema['properties'][propertyName]
    if 'default' in paramsSchema:
      options[propertyName] = paramsSchema['default']
    else:
      options[propertyName] = None