def _add_out_streams(self, spbl):
    """Adds outputs to a given protobuf Bolt or Spout message"""
    if self.outputs is None:
      return

    # sanitize outputs and get a map <stream_id -> out fields>
    output_map = self._sanitize_outputs()

    for stream_id, out_fields in output_map.items():
      out_stream = spbl.outputs.add()
      out_stream.stream.CopyFrom(self._get_stream_id(self.name, stream_id))
      out_stream.schema.CopyFrom(self._get_stream_schema(out_fields))