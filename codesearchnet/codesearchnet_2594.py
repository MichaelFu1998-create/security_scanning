def is_grouping_sane(cls, gtype):
    """Checks if a given gtype is sane"""
    if gtype == cls.SHUFFLE or gtype == cls.ALL or gtype == cls.LOWEST or gtype == cls.NONE:
      return True
    elif isinstance(gtype, cls.FIELDS):
      return gtype.gtype == topology_pb2.Grouping.Value("FIELDS") and \
             gtype.fields is not None
    elif isinstance(gtype, cls.CUSTOM):
      return gtype.gtype == topology_pb2.Grouping.Value("CUSTOM") and \
             gtype.python_serialized is not None
    else:
      #pylint: disable=fixme
      #TODO: DIRECT are not supported yet
      return False