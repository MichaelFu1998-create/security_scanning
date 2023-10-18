def _add_in_streams(self, bolt):
    """Adds inputs to a given protobuf Bolt message"""
    if self.inputs is None:
      return
    # sanitize inputs and get a map <GlobalStreamId -> Grouping>
    input_dict = self._sanitize_inputs()

    for global_streamid, gtype in input_dict.items():
      in_stream = bolt.inputs.add()
      in_stream.stream.CopyFrom(self._get_stream_id(global_streamid.component_id,
                                                    global_streamid.stream_id))
      if isinstance(gtype, Grouping.FIELDS):
        # it's a field grouping
        in_stream.gtype = gtype.gtype
        in_stream.grouping_fields.CopyFrom(self._get_stream_schema(gtype.fields))
      elif isinstance(gtype, Grouping.CUSTOM):
        # it's a custom grouping
        in_stream.gtype = gtype.gtype
        in_stream.custom_grouping_object = gtype.python_serialized
        in_stream.type = topology_pb2.CustomGroupingObjectType.Value("PYTHON_OBJECT")
      else:
        in_stream.gtype = gtype