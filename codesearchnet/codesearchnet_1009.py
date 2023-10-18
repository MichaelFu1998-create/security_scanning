def write(self, proto):
    """ 
    Writes serialized data to proto object.

    :param proto: (DynamicStructBuilder) Proto object
    """
    protoCells = proto.init('cells', self.numCells)

    for i in xrange(self.numCells):
      segments = self._cells[i]._segments
      protoSegments = protoCells[i].init('segments', len(segments))

      for j, segment in enumerate(segments):
        synapses = segment._synapses
        protoSynapses = protoSegments[j].init('synapses', len(synapses))

        for k, synapse in enumerate(sorted(synapses, key=lambda s: s._ordinal)):
          protoSynapses[k].presynapticCell = synapse.presynapticCell
          protoSynapses[k].permanence = synapse.permanence