def fields(cls, *fields):
    """Field grouping"""
    if len(fields) == 1 and isinstance(fields[0], list):
      fields = fields[0]
    else:
      fields = list(fields)

    for i in fields:
      if not isinstance(i, str):
        raise TypeError("Non-string cannot be specified in fields")

    if not fields:
      raise ValueError("List cannot be empty for fields grouping")

    return cls.FIELDS(gtype=topology_pb2.Grouping.Value("FIELDS"),
                      fields=fields)