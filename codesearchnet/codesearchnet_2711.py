def emit(self, tup, stream=Stream.DEFAULT_STREAM_ID,
           anchors=None, direct_task=None, need_task_ids=False):
    """Emits a new tuple from this Bolt

    It is compatible with StreamParse API.

    :type tup: list or tuple
    :param tup: the new output Tuple to send from this bolt,
                should only contain only serializable data.
    :type stream: str
    :param stream: the ID of the stream to emit this Tuple to.
                   Leave empty to emit to the default stream.
    :type anchors: list
    :param anchors: a list of HeronTuples to which the emitted Tuples should be anchored.
    :type direct_task: int
    :param direct_task: the task to send the Tupel to if performing a direct emit.
    :type need_task_ids: bool
    :param need_task_ids: indicate whether or not you would like the task IDs the Tuple was emitted.
    """
    # first check whether this tuple is sane
    self.pplan_helper.check_output_schema(stream, tup)

    # get custom grouping target task ids; get empty list if not custom grouping
    custom_target_task_ids = self.pplan_helper.choose_tasks_for_custom_grouping(stream, tup)

    self.pplan_helper.context.invoke_hook_emit(tup, stream, None)

    data_tuple = tuple_pb2.HeronDataTuple()
    data_tuple.key = 0

    if direct_task is not None:
      if not isinstance(direct_task, int):
        raise TypeError("direct_task argument needs to be an integer, given: %s"
                        % str(type(direct_task)))
      # performing emit-direct
      data_tuple.dest_task_ids.append(direct_task)
    elif custom_target_task_ids is not None:
      for task_id in custom_target_task_ids:
        # for custom grouping
        data_tuple.dest_task_ids.append(task_id)

    # Set the anchors for a tuple
    if anchors is not None:
      merged_roots = set()
      for tup in [t for t in anchors if isinstance(t, HeronTuple) and t.roots is not None]:
        merged_roots.update(tup.roots)
      for rt in merged_roots:
        to_add = data_tuple.roots.add()
        to_add.CopyFrom(rt)

    tuple_size_in_bytes = 0
    start_time = time.time()

    # Serialize
    for obj in tup:
      serialized = self.serializer.serialize(obj)
      data_tuple.values.append(serialized)
      tuple_size_in_bytes += len(serialized)
    serialize_latency_ns = (time.time() - start_time) * system_constants.SEC_TO_NS
    self.bolt_metrics.serialize_data_tuple(stream, serialize_latency_ns)

    super(BoltInstance, self).admit_data_tuple(stream_id=stream, data_tuple=data_tuple,
                                               tuple_size_in_bytes=tuple_size_in_bytes)

    self.bolt_metrics.update_emit_count(stream)
    if need_task_ids:
      sent_task_ids = custom_target_task_ids or []
      if direct_task is not None:
        sent_task_ids.append(direct_task)
      return sent_task_ids