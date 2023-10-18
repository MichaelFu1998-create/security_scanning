def write(self, proto):
    """Populate serialization proto instance.

    :param proto: (BacktrackingTMCppProto) the proto instance to populate
    """
    # Write base class to proto.baseTM (BacktrackingTMProto)
    super(BacktrackingTMCPP, self).write(proto.baseTM)
    self.cells4.write(proto.cells4)
    proto.makeCells4Ephemeral = self.makeCells4Ephemeral
    proto.seed = self.seed
    proto.checkSynapseConsistency = self.checkSynapseConsistency
    proto.initArgs = json.dumps(self._initArgsDict)