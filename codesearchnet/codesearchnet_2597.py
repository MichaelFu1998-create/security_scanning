def custom_serialized(cls, serialized, is_java=True):
    """Custom grouping from a given serialized string

    This class is created for compatibility with ``custom_serialized(cls, java_serialized)`` method
    of StreamParse API, although its functionality is not yet implemented (Java-serialized).
    Currently only custom grouping implemented in Python is supported, and ``custom()`` method
    should be used to indicate its classpath, rather than directly to use this method.

    In the future, users can directly specify Java-serialized object with ``is_java=True`` in order
    to use a custom grouping implemented in Java for python topology.

    :param serialized: serialized classpath to custom grouping class to use (if python)
    :param is_java: indicate whether this is Java serialized, or python serialized
    """
    if not isinstance(serialized, bytes):
      raise TypeError("Argument to custom_serialized() must be "
                      "a serialized Python class as bytes, given: %s" % str(serialized))
    if not is_java:
      return cls.CUSTOM(gtype=topology_pb2.Grouping.Value("CUSTOM"),
                        python_serialized=serialized)
    else:
      raise NotImplementedError("Custom grouping implemented in Java for Python topology"
                                "is not yet supported.")