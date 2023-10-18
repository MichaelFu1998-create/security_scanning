def decode(self, encoded, parentFieldName=""):
    """See the function description in base.py"""

    if parentFieldName != "":
      fieldName = "%s.%s" % (parentFieldName, self.name)
    else:
      fieldName = self.name

    return ({fieldName: ([[0, 0]], "input")}, [fieldName])