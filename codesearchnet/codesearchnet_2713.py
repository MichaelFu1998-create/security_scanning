def ack(self, tup):
    """Indicate that processing of a Tuple has succeeded

    It is compatible with StreamParse API.
    """
    if not isinstance(tup, HeronTuple):
      Log.error("Only HeronTuple type is supported in ack()")
      return

    if self.acking_enabled:
      ack_tuple = tuple_pb2.AckTuple()
      ack_tuple.ackedtuple = int(tup.id)

      tuple_size_in_bytes = 0
      for rt in tup.roots:
        to_add = ack_tuple.roots.add()
        to_add.CopyFrom(rt)
        tuple_size_in_bytes += rt.ByteSize()
      super(BoltInstance, self).admit_control_tuple(ack_tuple, tuple_size_in_bytes, True)

    process_latency_ns = (time.time() - tup.creation_time) * system_constants.SEC_TO_NS
    self.pplan_helper.context.invoke_hook_bolt_ack(tup, process_latency_ns)
    self.bolt_metrics.acked_tuple(tup.stream, tup.component, process_latency_ns)