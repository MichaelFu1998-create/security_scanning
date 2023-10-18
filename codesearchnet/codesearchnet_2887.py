def check_output_schema(self, stream_id, tup):
    """Checks if a given stream_id and tuple matches with the output schema

    :type stream_id: str
    :param stream_id: stream id into which tuple is sent
    :type tup: list
    :param tup: tuple that is going to be sent
    """
    # do some checking to make sure that the number of fields match what's expected
    size = self._output_schema.get(stream_id, None)
    if size is None:
      raise RuntimeError("%s emitting to stream %s but was not declared in output fields"
                         % (self.my_component_name, stream_id))
    elif size != len(tup):
      raise RuntimeError("Number of fields emitted in stream %s does not match what's expected. "
                         "Expected: %s, Observed: %s" % (stream_id, size, len(tup)))