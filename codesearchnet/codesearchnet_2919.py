def spec(cls, name=None, inputs=None, par=1, config=None, optional_outputs=None):
    """Register this bolt to the topology and create ``HeronComponentSpec``

    This method takes an optional ``outputs`` argument for supporting dynamic output fields
    declaration. However, it is recommended that ``outputs`` should be declared as
    an attribute of your ``Bolt`` subclass. Also, some ways of declaring inputs is not supported
    in this implementation; please read the documentation below.

    :type name: str
    :param name: Name of this bolt.
    :type inputs: dict or list
    :param inputs: Streams that feed into this Bolt.

                   Two forms of this are acceptable:

                   1. A `dict` mapping from ``HeronComponentSpec`` to ``Grouping``.
                      In this case, default stream is used.
                   2. A `dict` mapping from ``GlobalStreamId`` to ``Grouping``.
                      This ``GlobalStreamId`` object itself is different from StreamParse, because
                      Heron does not use thrift, although its constructor method is compatible.
                   3. A `list` of ``HeronComponentSpec``. In this case, default stream with
                      SHUFFLE grouping is used.
                   4. A `list` of ``GlobalStreamId``. In this case, SHUFFLE grouping is used.
    :type par: int
    :param par: Parallelism hint for this spout.
    :type config: dict
    :param config: Component-specific config settings.
    :type optional_outputs: list of (str or Stream) or tuple of (str or Stream)
    :param optional_outputs: Additional output fields for this bolt. These fields are added to
                             existing ``outputs`` class attributes of your bolt. This is an optional
                             argument, and exists only for supporting dynamic output field
                             declaration.
    """
    python_class_path = "%s.%s" % (cls.__module__, cls.__name__)

    if hasattr(cls, 'outputs'):
      # avoid modification to cls.outputs
      _outputs = copy.copy(cls.outputs)
    else:
      _outputs = []

    if optional_outputs is not None:
      assert isinstance(optional_outputs, (list, tuple))
      for out in optional_outputs:
        assert isinstance(out, (str, Stream))
        _outputs.append(out)

    return HeronComponentSpec(name, python_class_path, is_spout=False, par=par,
                              inputs=inputs, outputs=_outputs, config=config)