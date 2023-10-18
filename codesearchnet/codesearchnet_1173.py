def write(self, proto):
    """Populate serialization proto instance.

    :param proto: (TemporalMemoryShimProto) the proto instance to populate
    """
    super(TemporalMemoryShim, self).write(proto.baseTM)
    proto.connections.write(self.connections)
    proto.predictiveCells = self.predictiveCells