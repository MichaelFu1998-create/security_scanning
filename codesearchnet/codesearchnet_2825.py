def _get_base_component(self):
    """Returns Component protobuf message"""
    comp = topology_pb2.Component()
    comp.name = self.name
    comp.spec = topology_pb2.ComponentObjectSpec.Value("PYTHON_CLASS_NAME")
    comp.class_name = self.python_class_path
    comp.config.CopyFrom(self._get_comp_config())
    return comp