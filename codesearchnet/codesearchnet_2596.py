def custom(cls, customgrouper):
    """Custom grouping from a given implementation of ICustomGrouping

    :param customgrouper: The ICustomGrouping implemention to use
    """
    if customgrouper is None:
      raise TypeError("Argument to custom() must be ICustomGrouping instance or classpath")
    if not isinstance(customgrouper, ICustomGrouping) and not isinstance(customgrouper, str):
      raise TypeError("Argument to custom() must be ICustomGrouping instance or classpath")
    serialized = default_serializer.serialize(customgrouper)
    return cls.custom_serialized(serialized, is_java=False)