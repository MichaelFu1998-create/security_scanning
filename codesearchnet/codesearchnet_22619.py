def _ConvertFieldValuePair(js, message):
  """Convert field value pairs into regular message.

  Args:
    js: A JSON object to convert the field value pairs.
    message: A regular protocol message to record the data.

  Raises:
    ParseError: In case of problems converting.
  """
  names = []
  message_descriptor = message.DESCRIPTOR
  for name in js:
    try:
      field = message_descriptor.fields_by_camelcase_name.get(name, None)
      if not field:
        raise ParseError(
            'Message type "{0}" has no field named "{1}".'.format(
                message_descriptor.full_name, name))
      if name in names:
        raise ParseError(
            'Message type "{0}" should not have multiple "{1}" fields.'.format(
                message.DESCRIPTOR.full_name, name))
      names.append(name)
      # Check no other oneof field is parsed.
      if field.containing_oneof is not None:
        oneof_name = field.containing_oneof.name
        if oneof_name in names:
          raise ParseError('Message type "{0}" should not have multiple "{1}" '
                           'oneof fields.'.format(
                               message.DESCRIPTOR.full_name, oneof_name))
        names.append(oneof_name)

      value = js[name]
      if value is None:
        message.ClearField(field.name)
        continue

      # Parse field value.
      if _IsMapEntry(field):
        message.ClearField(field.name)
        _ConvertMapFieldValue(value, message, field)
      elif field.label == descriptor.FieldDescriptor.LABEL_REPEATED:
        message.ClearField(field.name)
        if not isinstance(value, list):
          raise ParseError('repeated field {0} must be in [] which is '
                           '{1}.'.format(name, value))
        if field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_MESSAGE:
          # Repeated message field.
          for item in value:
            sub_message = getattr(message, field.name).add()
            # None is a null_value in Value.
            if (item is None and
                sub_message.DESCRIPTOR.full_name != 'google.protobuf.Value'):
              raise ParseError('null is not allowed to be used as an element'
                               ' in a repeated field.')
            _ConvertMessage(item, sub_message)
        else:
          # Repeated scalar field.
          for item in value:
            if item is None:
              raise ParseError('null is not allowed to be used as an element'
                               ' in a repeated field.')
            getattr(message, field.name).append(
                _ConvertScalarFieldValue(item, field))
      elif field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_MESSAGE:
        sub_message = getattr(message, field.name)
        _ConvertMessage(value, sub_message)
      else:
        setattr(message, field.name, _ConvertScalarFieldValue(value, field))
    except ParseError as e:
      if field and field.containing_oneof is None:
        raise ParseError('Failed to parse {0} field: {1}'.format(name, e))
      else:
        raise ParseError(str(e))
    except ValueError as e:
      raise ParseError('Failed to parse {0} field: {1}.'.format(name, e))
    except TypeError as e:
      raise ParseError('Failed to parse {0} field: {1}.'.format(name, e))