def init_topology(mcs, classname, class_dict):
    """Initializes a topology protobuf"""
    if classname == 'Topology':
      # Base class can't initialize protobuf
      return
    heron_options = TopologyType.get_heron_options_from_env()
    initial_state = heron_options.get("cmdline.topology.initial.state", "RUNNING")
    tmp_directory = heron_options.get("cmdline.topologydefn.tmpdirectory")
    if tmp_directory is None:
      raise RuntimeError("Topology definition temp directory not specified")

    topology_name = heron_options.get("cmdline.topology.name", classname)
    topology_id = topology_name + str(uuid.uuid4())

    # create protobuf
    topology = topology_pb2.Topology()
    topology.id = topology_id
    topology.name = topology_name
    topology.state = topology_pb2.TopologyState.Value(initial_state)
    topology.topology_config.CopyFrom(TopologyType.get_topology_config_protobuf(class_dict))

    TopologyType.add_bolts_and_spouts(topology, class_dict)

    class_dict['topology_name'] = topology_name
    class_dict['topology_id'] = topology_id
    class_dict['protobuf_topology'] = topology
    class_dict['topologydefn_tmpdir'] = tmp_directory
    class_dict['heron_runtime_options'] = heron_options