def _getInputValue(self, obj, fieldName):
    """
    Gets the value of a given field from the input record
    """
    if isinstance(obj, dict):
      if not fieldName in obj:
        knownFields = ", ".join(
          key for key in obj.keys() if not key.startswith("_")
        )
        raise ValueError(
          "Unknown field name '%s' in input record. Known fields are '%s'.\n"
          "This could be because input headers are mislabeled, or because "
          "input data rows do not contain a value for '%s'." % (
            fieldName, knownFields, fieldName
          )
        )
      return obj[fieldName]
    else:
      return getattr(obj, fieldName)