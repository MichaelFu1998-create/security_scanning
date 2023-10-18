def PrintFieldValue(self, field, value):
    """Print a single field value (not including name).

    For repeated fields, the value should be a single element.

    Args:
      field: The descriptor of the field to be printed.
      value: The value of the field.
    """
    out = self.out
    if self.pointy_brackets:
      openb = '<'
      closeb = '>'
    else:
      openb = '{'
      closeb = '}'

    if field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_MESSAGE:
      if self.as_one_line:
        out.write(' %s ' % openb)
        self.PrintMessage(value)
        out.write(closeb)
      else:
        out.write(' %s\n' % openb)
        self.indent += 2
        self.PrintMessage(value)
        self.indent -= 2
        out.write(' ' * self.indent + closeb)
    elif field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_ENUM:
      enum_value = field.enum_type.values_by_number.get(value, None)
      if enum_value is not None:
        out.write(enum_value.name)
      else:
        out.write(str(value))
    elif field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_STRING:
      out.write('\"')
      if isinstance(value, six.text_type):
        out_value = value.encode('utf-8')
      else:
        out_value = value
      if field.type == descriptor.FieldDescriptor.TYPE_BYTES:
        # We need to escape non-UTF8 chars in TYPE_BYTES field.
        out_as_utf8 = False
      else:
        out_as_utf8 = self.as_utf8
      out.write(text_encoding.CEscape(out_value, out_as_utf8))
      out.write('\"')
    elif field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_BOOL:
      if value:
        out.write('true')
      else:
        out.write('false')
    elif field.cpp_type in _FLOAT_TYPES and self.float_format is not None:
      out.write('{1:{0}}'.format(self.float_format, value))
    else:
      out.write(str(value))