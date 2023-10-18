def addMultipleFields(self, fieldsInfo):
    """Add multiple fields to the dataset.
    Parameters:
    -------------------------------------------------------------------
    fieldsInfo:       A list of dictionaries, containing a field name, specs for
                      the data classes and encoder params for the corresponding
                      field.
    """
    assert all(x in field for x in ['name', 'fieldSpec', 'encoderParams'] for field \
               in fieldsInfo)

    for spec in fieldsInfo:
      self.addField(spec.pop('name'), spec.pop('fieldSpec'), spec.pop('encoderParams'))