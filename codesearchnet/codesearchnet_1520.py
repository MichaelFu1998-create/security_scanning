def _getFieldIndexBySpecial(fields, special):
  """ Return index of the field matching the field meta special value.
  :param fields: sequence of nupic.data.fieldmeta.FieldMetaInfo objects
    representing the fields of a stream
  :param special: one of the special field attribute values from
    nupic.data.fieldmeta.FieldMetaSpecial
  :returns: first zero-based index of the field tagged with the target field
    meta special attribute; None if no such field
  """
  for i, field in enumerate(fields):
    if field.special == special:
      return i
  return None