def do_classdesc(self, parent=None, ident=0):
    """do_classdesc"""
    # TC_CLASSDESC className serialVersionUID newHandle classDescInfo
    # classDescInfo:
    #   classDescFlags fields classAnnotation superClassDesc
    # classDescFlags:
    #   (byte)                  // Defined in Terminal Symbols and Constants
    # fields:
    #   (short)<count>  fieldDesc[count]

    # fieldDesc:
    #   primitiveDesc
    #   objectDesc
    # primitiveDesc:
    #   prim_typecode fieldName
    # objectDesc:
    #   obj_typecode fieldName className1
    clazz = JavaClass()
    log_debug("[classdesc]", ident)
    ba = self._readString()
    clazz.name = ba
    log_debug("Class name: %s" % ba, ident)
    (serialVersionUID, newHandle, classDescFlags) = self._readStruct(">LLB")
    clazz.serialVersionUID = serialVersionUID
    clazz.flags = classDescFlags

    self._add_reference(clazz)

    log_debug("Serial: 0x%X newHandle: 0x%X.\
classDescFlags: 0x%X" % (serialVersionUID, newHandle, classDescFlags), ident)
    (length, ) = self._readStruct(">H")
    log_debug("Fields num: 0x%X" % length, ident)

    clazz.fields_names = []
    clazz.fields_types = []
    for _ in range(length):
      (typecode, ) = self._readStruct(">B")
      field_name = self._readString()
      field_type = None
      field_type = self._convert_char_to_type(typecode)

      if field_type == self.TYPE_ARRAY:
        _, field_type = self._read_and_exec_opcode(
            ident=ident+1, expect=[self.TC_STRING, self.TC_REFERENCE])
        assert isinstance(field_type, str)
#              if field_type is not None:
#                  field_type = "array of " + field_type
#              else:
#                  field_type = "array of None"
      elif field_type == self.TYPE_OBJECT:
        _, field_type = self._read_and_exec_opcode(
            ident=ident+1, expect=[self.TC_STRING, self.TC_REFERENCE])
        assert isinstance(field_type, str)

      log_debug("FieldName: 0x%X" % typecode + " " + str(field_name) + " " + str(field_type), ident)
      assert field_name is not None
      assert field_type is not None

      clazz.fields_names.append(field_name)
      clazz.fields_types.append(field_type)
    # pylint: disable=protected-access
    if parent:
      parent.__fields = clazz.fields_names
      parent.__types = clazz.fields_types
    # classAnnotation
    (opid, ) = self._readStruct(">B")
    log_debug("OpCode: 0x%X" % opid, ident)
    if opid != self.TC_ENDBLOCKDATA:
      raise NotImplementedError("classAnnotation isn't implemented yet")
    # superClassDesc
    _, superclassdesc = self._read_and_exec_opcode(
        ident=ident+1, expect=[self.TC_CLASSDESC, self.TC_NULL, self.TC_REFERENCE])
    log_debug(str(superclassdesc), ident)
    clazz.superclass = superclassdesc

    return clazz