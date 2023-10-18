def extract_logical_plan(self, topology):
    """
    Returns the representation of logical plan that will
    be returned from Tracker.
    """
    logicalPlan = {
        "spouts": {},
        "bolts": {},
    }

    # Add spouts.
    for spout in topology.spouts():
      spoutName = spout.comp.name
      spoutType = "default"
      spoutSource = "NA"
      spoutVersion = "NA"
      spoutConfigs = spout.comp.config.kvs
      for kvs in spoutConfigs:
        if kvs.key == "spout.type":
          spoutType = javaobj.loads(kvs.serialized_value)
        elif kvs.key == "spout.source":
          spoutSource = javaobj.loads(kvs.serialized_value)
        elif kvs.key == "spout.version":
          spoutVersion = javaobj.loads(kvs.serialized_value)
      spoutPlan = {
          "config": convert_pb_kvs(spoutConfigs, include_non_primitives=False),
          "type": spoutType,
          "source": spoutSource,
          "version": spoutVersion,
          "outputs": []
      }
      for outputStream in list(spout.outputs):
        spoutPlan["outputs"].append({
            "stream_name": outputStream.stream.id
        })

      logicalPlan["spouts"][spoutName] = spoutPlan

    # Add bolts.
    for bolt in topology.bolts():
      boltName = bolt.comp.name
      boltPlan = {
          "config": convert_pb_kvs(bolt.comp.config.kvs, include_non_primitives=False),
          "outputs": [],
          "inputs": []
      }
      for outputStream in list(bolt.outputs):
        boltPlan["outputs"].append({
            "stream_name": outputStream.stream.id
        })
      for inputStream in list(bolt.inputs):
        boltPlan["inputs"].append({
            "stream_name": inputStream.stream.id,
            "component_name": inputStream.stream.component_name,
            "grouping": topology_pb2.Grouping.Name(inputStream.gtype)
        })

      logicalPlan["bolts"][boltName] = boltPlan

    return logicalPlan