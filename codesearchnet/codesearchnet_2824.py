def _get_bolt(self):
    """Returns Bolt protobuf message"""
    bolt = topology_pb2.Bolt()
    bolt.comp.CopyFrom(self._get_base_component())

    # Add streams
    self._add_in_streams(bolt)
    self._add_out_streams(bolt)
    return bolt