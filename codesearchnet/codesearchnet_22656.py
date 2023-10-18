def PrintMessage(self, message):
    """Convert protobuf message to text format.

    Args:
      message: The protocol buffers message.
    """
    fields = message.ListFields()
    if self.use_index_order:
      fields.sort(key=lambda x: x[0].index)
    for field, value in fields:
      if _IsMapEntry(field):
        for key in sorted(value):
          # This is slow for maps with submessage entires because it copies the
          # entire tree.  Unfortunately this would take significant refactoring
          # of this file to work around.
          #
          # TODO(haberman): refactor and optimize if this becomes an issue.
          entry_submsg = field.message_type._concrete_class(
              key=key, value=value[key])
          self.PrintField(field, entry_submsg)
      elif field.label == descriptor.FieldDescriptor.LABEL_REPEATED:
        for element in value:
          self.PrintField(field, element)
      else:
        self.PrintField(field, value)