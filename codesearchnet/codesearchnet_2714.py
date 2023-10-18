def fail(self, tup):
    """Indicate that processing of a Tuple has failed

    It is compatible with StreamParse API.
    """
    if not isinstance(tup, HeronTuple):
      Log.error("Only HeronTuple type is supported in fail()")
      return

    if self.acking_enabled:
      fail_tuple = tuple_pb2.AckTuple()
      fail_tuple.ackedtuple = int(tup.id)

      tuple_size_in_bytes = 0
      for rt in tup.roots:
        to_add = fail_tuple.roots.add()
        to_add.CopyFrom(rt)
        tuple_size_in_bytes += rt.ByteSize()
      super(BoltInstance, self).admit_control_tuple(fail_tuple, tuple_size_in_bytes, False)

    fail_latency_ns = (time.time() - tup.creation_time) * system_constants.SEC_TO_NS
    self.pplan_helper.context.invoke_hook_bolt_fail(tup, fail_latency_ns)
    self.bolt_metrics.failed_tuple(tup.stream, tup.component, fail_latency_ns)