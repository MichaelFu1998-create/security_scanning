def readFromCheckpoint(cls, checkpointDir):
    """Deserializes model from checkpointDir using capnproto"""
    checkpointPath = cls._getModelCheckpointFilePath(checkpointDir)

    with open(checkpointPath, 'r') as f:
      proto = cls.getSchema().read(f,
                                   traversal_limit_in_words=_TRAVERSAL_LIMIT_IN_WORDS)

    model = cls.read(proto)
    return model