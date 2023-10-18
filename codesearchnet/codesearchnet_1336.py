def read(cls, proto):
    """
    Intercepts TemporalMemory deserialization request in order to initialize
    `TemporalMemoryMonitorMixin` state

    @param proto (DynamicStructBuilder) Proto object

    @return (TemporalMemory) TemporalMemory shim instance
    """
    tm = super(TemporalMemoryMonitorMixin, cls).read(proto)

    # initialize `TemporalMemoryMonitorMixin` attributes
    tm.mmName = None
    tm._mmTraces = None
    tm._mmData = None
    tm.mmClearHistory()
    tm._mmResetActive = True
    return tm