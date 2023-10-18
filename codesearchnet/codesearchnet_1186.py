def write(self, proto):
    """
    :param proto: capnp TwoGramModelProto message builder
    """
    super(TwoGramModel, self).writeBaseToProto(proto.modelBase)

    proto.reset = self._reset
    proto.learningEnabled = self._learningEnabled
    proto.prevValues = self._prevValues
    self._encoder.write(proto.encoder)
    proto.hashToValueDict = [{"hash": h, "value": v}
                             for h, v in self._hashToValueDict.items()]

    twoGramDicts = []
    for items in self._twoGramDicts:
      twoGramArr = []
      for prev, values in items.iteritems():
        buckets = [{"index": index, "count": count}
                   for index, count in values.iteritems()]
        if prev is None:
          prev = -1
        twoGramArr.append({"value": prev, "buckets": buckets})

      twoGramDicts.append(twoGramArr)

    proto.twoGramDicts = twoGramDicts