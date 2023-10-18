def _setup_custom_grouping(self, topology):
    """Checks whether there are any bolts that consume any of my streams using custom grouping"""
    for i in range(len(topology.bolts)):
      for in_stream in topology.bolts[i].inputs:
        if in_stream.stream.component_name == self.my_component_name and \
          in_stream.gtype == topology_pb2.Grouping.Value("CUSTOM"):
          # this bolt takes my output in custom grouping manner
          if in_stream.type == topology_pb2.CustomGroupingObjectType.Value("PYTHON_OBJECT"):
            custom_grouping_obj = default_serializer.deserialize(in_stream.custom_grouping_object)
            if isinstance(custom_grouping_obj, str):
              pex_loader.load_pex(self.topology_pex_abs_path)
              grouping_cls = \
                pex_loader.import_and_get_class(self.topology_pex_abs_path, custom_grouping_obj)
              custom_grouping_obj = grouping_cls()
            assert isinstance(custom_grouping_obj, ICustomGrouping)
            self.custom_grouper.add(in_stream.stream.id,
                                    self._get_taskids_for_component(topology.bolts[i].comp.name),
                                    custom_grouping_obj,
                                    self.my_component_name)

          elif in_stream.type == topology_pb2.CustomGroupingObjectType.Value("JAVA_OBJECT"):
            raise NotImplementedError("Java-serialized custom grouping is not yet supported "
                                      "for python topology")
          else:
            raise ValueError("Unrecognized custom grouping type found: %s" % str(in_stream.type))