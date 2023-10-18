def handle_new_tuple_set_2(self, hts2):
    """Called when new HeronTupleSet2 arrives
       Convert(Assemble) HeronTupleSet2(raw byte array) to HeronTupleSet
       See more at GitHub PR #1421
    :param tuple_msg_set: HeronTupleSet2 type
    """
    if self.my_pplan_helper is None or self.my_instance is None:
      Log.error("Got tuple set when no instance assigned yet")
    else:
      hts = tuple_pb2.HeronTupleSet()
      if hts2.HasField('control'):
        hts.control.CopyFrom(hts2.control)
      else:
        hdts = tuple_pb2.HeronDataTupleSet()
        hdts.stream.CopyFrom(hts2.data.stream)
        try:
          for trunk in hts2.data.tuples:
            added_tuple = hdts.tuples.add()
            added_tuple.ParseFromString(trunk)
        except Exception:
          Log.exception('Fail to deserialize HeronDataTuple')
        hts.data.CopyFrom(hdts)
      self.in_stream.offer(hts)
      if self.my_pplan_helper.is_topology_running():
        self.my_instance.py_class.process_incoming_tuples()