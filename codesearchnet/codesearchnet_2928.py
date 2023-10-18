def make_tick_tuple():
    """Creates a TickTuple"""
    return HeronTuple(id=TupleHelper.TICK_TUPLE_ID, component=TupleHelper.TICK_SOURCE_COMPONENT,
                      stream=TupleHelper.TICK_TUPLE_ID, task=None, values=None,
                      creation_time=time.time(), roots=None)