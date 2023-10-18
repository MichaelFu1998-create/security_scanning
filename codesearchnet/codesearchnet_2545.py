def emit(self, tup, tup_id=None, stream=Stream.DEFAULT_STREAM_ID,
           direct_task=None, need_task_ids=False):
    """Emits a new tuple from this Spout

    It is compatible with StreamParse API.

    :type tup: list or tuple
    :param tup: the new output Tuple to send from this spout,
                should contain only serializable data.
    :type tup_id: str or object
    :param tup_id: the ID for the Tuple. Leave this blank for an unreliable emit.
                   (Same as messageId in Java)
    :type stream: str
    :param stream: the ID of the stream this Tuple should be emitted to.
                   Leave empty to emit to the default stream.
    :type direct_task: int
    :param direct_task: the task to send the Tuple to if performing a direct emit.
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
      # for custom grouping
      for task_id in custom_target_task_ids:
        data_tuple.dest_task_ids.append(task_id)

    if tup_id is not None:
      tuple_info = TupleHelper.make_root_tuple_info(stream, tup_id)
      if self.acking_enabled:
        # this message is rooted
        root = data_tuple.roots.add()
        root.taskid = self.pplan_helper.my_task_id
        root.key = tuple_info.key
        self.in_flight_tuples[tuple_info.key] = tuple_info
      else:
        self.immediate_acks.append(tuple_info)

    tuple_size_in_bytes = 0

    start_time = time.time()

    # Serialize
    for obj in tup:
      serialized = self.serializer.serialize(obj)
      data_tuple.values.append(serialized)
      tuple_size_in_bytes += len(serialized)

    serialize_latency_ns = (time.time() - start_time) * system_constants.SEC_TO_NS
    self.spout_metrics.serialize_data_tuple(stream, serialize_latency_ns)

    super(SpoutInstance, self).admit_data_tuple(stream_id=stream, data_tuple=data_tuple,
                                                tuple_size_in_bytes=tuple_size_in_bytes)
    self.total_tuples_emitted += 1
    self.spout_metrics.update_emit_count(stream)
    if need_task_ids:
      sent_task_ids = custom_target_task_ids or []
      if direct_task is not None:
        sent_task_ids.append(direct_task)
      return sent_task_ids