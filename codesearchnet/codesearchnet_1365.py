def getDecoderOutputFieldTypes(self):
    """
    Returns a sequence of field types corresponding to the elements in the
    decoded output field array.  The types are defined by
    :class:`~nupic.data.field_meta.FieldMetaType`.

    :return: list of :class:`~nupic.data.field_meta.FieldMetaType` objects
    """
    if hasattr(self, '_flattenedFieldTypeList') and \
          self._flattenedFieldTypeList is not None:
      return self._flattenedFieldTypeList

    fieldTypes = []

    # NOTE: we take care of the composites, but leaf encoders must override
    #       this method and return a list of one field_meta.FieldMetaType.XXXX
    #       element corresponding to the encoder's decoder output field type
    for (name, encoder, offset) in self.encoders:
      subTypes = encoder.getDecoderOutputFieldTypes()
      fieldTypes.extend(subTypes)

    self._flattenedFieldTypeList = fieldTypes
    return fieldTypes