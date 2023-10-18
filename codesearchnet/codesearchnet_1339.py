def read(cls, proto):
    """
    Intercepts TemporalMemory deserialization request in order to initialize
    `self.infActiveState`

    @param proto (DynamicStructBuilder) Proto object

    @return (TemporalMemory) TemporalMemory shim instance
    """
    tm = super(MonitoredTMShim, cls).read(proto)
    tm.infActiveState = {"t": None}
    return tm