def consume(self, consume_function):
    """Calls consume_function for each element of this streamlet. This function returns nothing
    """
    from heronpy.streamlet.impl.consumebolt import ConsumeStreamlet
    consume_streamlet = ConsumeStreamlet(consume_function, self)
    self._add_child(consume_streamlet)
    return