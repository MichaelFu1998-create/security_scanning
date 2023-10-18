def read(cls, proto):
    """
    :param proto: capnp TwoGramModelProto message reader
    """
    instance = object.__new__(cls)
    super(TwoGramModel, instance).__init__(proto=proto.modelBase)

    instance._logger = opf_utils.initLogger(instance)

    instance._reset = proto.reset
    instance._hashToValueDict = {x.hash: x.value
                                 for x in proto.hashToValueDict}
    instance._learningEnabled = proto.learningEnabled
    instance._encoder = encoders.MultiEncoder.read(proto.encoder)
    instance._fieldNames = instance._encoder.getScalarNames()
    instance._prevValues = list(proto.prevValues)
    instance._twoGramDicts = [dict() for _ in xrange(len(proto.twoGramDicts))]
    for idx, field in enumerate(proto.twoGramDicts):
      for entry in field:
        prev = None if entry.value == -1 else entry.value
        instance._twoGramDicts[idx][prev] = collections.defaultdict(int)
        for bucket in entry.buckets:
          instance._twoGramDicts[idx][prev][bucket.index] = bucket.count

    return instance