def decode(self, encoded, parentFieldName=''):
    """
    Takes an encoded output and does its best to work backwards and generate
    the input that would have generated it.

    In cases where the encoded output contains more ON bits than an input
    would have generated, this routine will return one or more ranges of inputs
    which, if their encoded outputs were ORed together, would produce the
    target output. This behavior makes this method suitable for doing things
    like generating a description of a learned coincidence in the SP, which
    in many cases might be a union of one or more inputs.

    If instead, you want to figure the *most likely* single input scalar value
    that would have generated a specific encoded output, use the
    :meth:`.topDownCompute` method.

    If you want to pretty print the return value from this method, use the
    :meth:`.decodedToStr` method.

    :param encoded:      The encoded output that you want decode
    :param parentFieldName: The name of the encoder which is our parent. This name
           is prefixed to each of the field names within this encoder to form the
           keys of the dict() in the retval.

    :return: tuple(``fieldsDict``, ``fieldOrder``)

              ``fieldsDict`` is a dict() where the keys represent field names
              (only 1 if this is a simple encoder, > 1 if this is a multi
              or date encoder) and the values are the result of decoding each
              field. If there are  no bits in encoded that would have been
              generated by a field, it won't be present in the dict. The
              key of each entry in the dict is formed by joining the passed in
              parentFieldName with the child encoder name using a '.'.

              Each 'value' in ``fieldsDict`` consists of (ranges, desc), where
              ranges is a list of one or more (minVal, maxVal) ranges of
              input that would generate bits in the encoded output and 'desc'
              is a pretty print description of the ranges. For encoders like
              the category encoder, the 'desc' will contain the category
              names that correspond to the scalar values included in the
              ranges.

              ``fieldOrder`` is a list of the keys from ``fieldsDict``, in the
              same order as the fields appear in the encoded output.

              TODO: when we switch to Python 2.7 or 3.x, use OrderedDict

    Example retvals for a scalar encoder:

    .. code-block:: python

       {'amount':  ( [[1,3], [7,10]], '1-3, 7-10' )}
       {'amount':  ( [[2.5,2.5]],     '2.5'       )}

    Example retval for a category encoder:

    .. code-block:: python

       {'country': ( [[1,1], [5,6]], 'US, GB, ES' )}

    Example retval for a multi encoder:

    .. code-block:: python

       {'amount':  ( [[2.5,2.5]],     '2.5'       ),
        'country': ( [[1,1], [5,6]],  'US, GB, ES' )}

    """

    fieldsDict = dict()
    fieldsOrder = []

    # What is the effective parent name?
    if parentFieldName == '':
      parentName = self.name
    else:
      parentName = "%s.%s" % (parentFieldName, self.name)

    if self.encoders is not None:
      # Merge decodings of all child encoders together
      for i in xrange(len(self.encoders)):

        # Get the encoder and the encoded output
        (name, encoder, offset) = self.encoders[i]
        if i < len(self.encoders)-1:
          nextOffset = self.encoders[i+1][2]
        else:
          nextOffset = self.width
        fieldOutput = encoded[offset:nextOffset]
        (subFieldsDict, subFieldsOrder) = encoder.decode(fieldOutput,
                                              parentFieldName=parentName)

        fieldsDict.update(subFieldsDict)
        fieldsOrder.extend(subFieldsOrder)


    return (fieldsDict, fieldsOrder)