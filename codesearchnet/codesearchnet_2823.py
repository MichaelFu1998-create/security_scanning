def _get_spout(self):
    """Returns Spout protobuf message"""
    spout = topology_pb2.Spout()
    spout.comp.CopyFrom(self._get_base_component())

    # Add output streams
    self._add_out_streams(spout)
    return spout