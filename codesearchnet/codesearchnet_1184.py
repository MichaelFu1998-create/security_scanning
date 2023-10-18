def writeToFile(self, f, packed=True):
    """
    Write serialized object to file.

    :param f: output file
    :param packed: If true, will pack contents.
    """
    # Get capnproto schema from instance
    schema = self.getSchema()

    # Construct new message, otherwise refered to as `proto`
    proto = schema.new_message()

    # Populate message w/ `write()` instance method
    self.write(proto)

    # Finally, write to file
    if packed:
      proto.write_packed(f)
    else:
      proto.write(f)