def log(self):
    """Logs all elements of this streamlet. This returns nothing
    """
    from heronpy.streamlet.impl.logbolt import LogStreamlet
    log_streamlet = LogStreamlet(self)
    self._add_child(log_streamlet)
    return