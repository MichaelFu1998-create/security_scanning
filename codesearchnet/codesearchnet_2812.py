def build_and_submit(self):
    """Builds the topology and submits to the destination"""
    class_dict = self._construct_topo_class_dict()
    topo_cls = TopologyType(self.topology_name, (Topology,), class_dict)
    topo_cls.write()