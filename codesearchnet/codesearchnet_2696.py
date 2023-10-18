def get_serializer(context):
    """Returns a serializer for a given context"""
    cluster_config = context.get_cluster_config()
    serializer_clsname = cluster_config.get(constants.TOPOLOGY_SERIALIZER_CLASSNAME, None)
    if serializer_clsname is None:
      return PythonSerializer()
    else:
      try:
        topo_pex_path = context.get_topology_pex_path()
        pex_loader.load_pex(topo_pex_path)
        serializer_cls = pex_loader.import_and_get_class(topo_pex_path, serializer_clsname)
        serializer = serializer_cls()
        return serializer
      except Exception as e:
        raise RuntimeError("Error with loading custom serializer class: %s, with error message: %s"
                           % (serializer_clsname, str(e)))