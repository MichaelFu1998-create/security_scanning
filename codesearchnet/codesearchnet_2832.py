def get_out_streamids(self):
    """Returns a set of output stream ids registered for this component"""
    if self.outputs is None:
      return set()

    if not isinstance(self.outputs, (list, tuple)):
      raise TypeError("Argument to outputs must be either list or tuple, given: %s"
                      % str(type(self.outputs)))
    ret_lst = []
    for output in self.outputs:
      if not isinstance(output, (str, Stream)):
        raise TypeError("Outputs must be a list of strings or Streams, given: %s" % str(output))
      ret_lst.append(Stream.DEFAULT_STREAM_ID if isinstance(output, str) else output.stream_id)
    return set(ret_lst)