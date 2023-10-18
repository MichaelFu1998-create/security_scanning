def _sanitize_outputs(self):
    """Sanitizes output fields and returns a map <stream_id -> list of output fields>"""
    ret = {}
    if self.outputs is None:
      return

    if not isinstance(self.outputs, (list, tuple)):
      raise TypeError("Argument to outputs must be either list or tuple, given: %s"
                      % str(type(self.outputs)))

    for output in self.outputs:
      if not isinstance(output, (str, Stream)):
        raise TypeError("Outputs must be a list of strings or Streams, given: %s" % str(output))

      if isinstance(output, str):
        # it's a default stream
        if Stream.DEFAULT_STREAM_ID not in ret:
          ret[Stream.DEFAULT_STREAM_ID] = list()
        ret[Stream.DEFAULT_STREAM_ID].append(output)
      else:
        # output is a Stream object
        if output.stream_id == Stream.DEFAULT_STREAM_ID and Stream.DEFAULT_STREAM_ID in ret:
          # some default stream fields are already in there
          ret[Stream.DEFAULT_STREAM_ID].extend(output.fields)
        else:
          ret[output.stream_id] = output.fields
    return ret