def make_tuple(stream, tuple_key, values, roots=None):
    """Creates a HeronTuple

    :param stream: protobuf message ``StreamId``
    :param tuple_key: tuple id
    :param values: a list of values
    :param roots: a list of protobuf message ``RootId``
    """
    component_name = stream.component_name
    stream_id = stream.id
    gen_task = roots[0].taskid if roots is not None and len(roots) > 0 else None
    return HeronTuple(id=str(tuple_key), component=component_name, stream=stream_id,
                      task=gen_task, values=values, creation_time=time.time(), roots=roots)