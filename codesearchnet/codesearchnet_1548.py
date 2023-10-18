def writeToCheckpoint(self, checkpointDir):
    """Serializes model using capnproto and writes data to ``checkpointDir``"""
    proto = self.getSchema().new_message()

    self.write(proto)

    checkpointPath = self._getModelCheckpointFilePath(checkpointDir)

    # Clean up old saved state, if any
    if os.path.exists(checkpointDir):
      if not os.path.isdir(checkpointDir):
        raise Exception(("Existing filesystem entry <%s> is not a model"
                         " checkpoint -- refusing to delete (not a directory)") \
                          % checkpointDir)
      if not os.path.isfile(checkpointPath):
        raise Exception(("Existing filesystem entry <%s> is not a model"
                         " checkpoint -- refusing to delete"\
                         " (%s missing or not a file)") % \
                          (checkpointDir, checkpointPath))

      shutil.rmtree(checkpointDir)

    # Create a new directory for saving state
    self.__makeDirectoryFromAbsolutePath(checkpointDir)

    with open(checkpointPath, 'wb') as f:
      proto.write(f)