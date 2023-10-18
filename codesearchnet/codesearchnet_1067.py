def addField(self, name, fieldParams, encoderParams):
    """Add a single field to the dataset.
    Parameters:
    -------------------------------------------------------------------
    name:             The user-specified name of the field
    fieldSpec:        A list of one or more dictionaries specifying parameters
                      to be used for dataClass initialization. Each dict must
                      contain the key 'type' that specifies a distribution for
                      the values in this field
    encoderParams:    Parameters for the field encoder
    """

    assert fieldParams is not None and'type' in fieldParams

    dataClassName = fieldParams.pop('type')
    try:
      dataClass=eval(dataClassName)(fieldParams)

    except TypeError, e:
      print ("#### Error in constructing %s class object. Possibly missing "
              "some required constructor parameters. Parameters "
              "that were provided are: %s" % (dataClass, fieldParams))
      raise

    encoderParams['dataClass']=dataClass
    encoderParams['dataClassName']=dataClassName

    fieldIndex = self.defineField(name, encoderParams)