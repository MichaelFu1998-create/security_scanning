def _sanitize_inputs(self):
    """Sanitizes input fields and returns a map <GlobalStreamId -> Grouping>"""
    ret = {}
    if self.inputs is None:
      return

    if isinstance(self.inputs, dict):
      # inputs are dictionary, must be either <HeronComponentSpec -> Grouping> or
      # <GlobalStreamId -> Grouping>
      for key, grouping in self.inputs.items():
        if not Grouping.is_grouping_sane(grouping):
          raise ValueError('A given grouping is not supported')
        if isinstance(key, HeronComponentSpec):
          # use default streamid
          if key.name is None:
            # should not happen as TopologyType metaclass sets name attribute
            # before calling this method
            raise RuntimeError("In _sanitize_inputs(): HeronComponentSpec doesn't have a name")
          global_streamid = GlobalStreamId(key.name, Stream.DEFAULT_STREAM_ID)
          ret[global_streamid] = grouping
        elif isinstance(key, GlobalStreamId):
          ret[key] = grouping
        else:
          raise ValueError("%s is not supported as a key to inputs" % str(key))
    elif isinstance(self.inputs, (list, tuple)):
      # inputs are lists, must be either a list of HeronComponentSpec or GlobalStreamId
      # will use SHUFFLE grouping
      for input_obj in self.inputs:
        if isinstance(input_obj, HeronComponentSpec):
          if input_obj.name is None:
            # should not happen as TopologyType metaclass sets name attribute
            # before calling this method
            raise RuntimeError("In _sanitize_inputs(): HeronComponentSpec doesn't have a name")
          global_streamid = GlobalStreamId(input_obj.name, Stream.DEFAULT_STREAM_ID)
          ret[global_streamid] = Grouping.SHUFFLE
        elif isinstance(input_obj, GlobalStreamId):
          ret[input_obj] = Grouping.SHUFFLE
        else:
          raise ValueError("%s is not supported as an input" % str(input_obj))
    else:
      raise TypeError("Inputs must be a list, dict, or None, given: %s" % str(self.inputs))

    return ret