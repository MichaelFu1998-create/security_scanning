def read(cls, proto):
    """Deserialize from proto instance.

    :param proto: (BacktrackingTMCppProto) the proto instance to read from
    """
    # Use base class to create initial class from proto.baseTM
    # (BacktrackingTMProto)
    obj = BacktrackingTM.read(proto.baseTM)
    obj.__class__ = cls

    # Additional CPP-specific deserialization
    newCells4 = Cells4.read(proto.cells4)
    print newCells4
    obj.cells4 = newCells4
    obj.makeCells4Ephemeral = proto.makeCells4Ephemeral
    obj.seed = proto.seed
    obj.checkSynapseConsistency = proto.checkSynapseConsistency
    obj._initArgsDict = json.loads(proto.initArgs)
    # Convert unicode to str
    obj._initArgsDict["outputType"] = str(obj._initArgsDict["outputType"])

    # Initialize ephemeral attributes
    obj.allocateStatesInCPP = False
    obj.retrieveLearningStates = False
    obj._setStatePointers()

    return obj