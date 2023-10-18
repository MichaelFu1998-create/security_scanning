def emit(self, tup, stream=Stream.DEFAULT_STREAM_ID,
           anchors=None, direct_task=None, need_task_ids=False):
    """Emits a new tuple from this Bolt

    It is compatible with StreamParse API.

    :type tup: list or tuple
    :param tup: the new output Tuple to send from this bolt,
                which should contain only serializable data.
    :type stream: str
    :param stream: the ID of the stream to emit this Tuple to.
                   Leave empty to emit to the default stream.
    :type anchors: list
    :param anchors: a list of HeronTuples to which the emitted Tuples should be anchored.
    :type direct_task: int
    :param direct_task: the task to send the Tuple to if performing a direct emit.
    :type need_task_ids: bool
    :param need_task_ids: indicate whether or not you would like the task IDs the Tuple was emitted.
    """
    self.delegate.emit(tup, stream, anchors, direct_task, need_task_ids)