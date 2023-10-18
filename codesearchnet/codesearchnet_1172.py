def read(cls, proto):
    """Deserialize from proto instance.

    :param proto: (TemporalMemoryShimProto) the proto instance to read from
    """
    tm = super(TemporalMemoryShim, cls).read(proto.baseTM)
    tm.predictiveCells = set(proto.predictedState)
    tm.connections = Connections.read(proto.conncetions)