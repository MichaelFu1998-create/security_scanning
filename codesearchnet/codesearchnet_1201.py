def _serializeExtraData(self, extraDataDir):
    """ [virtual method override] This method is called during serialization
    with an external directory path that can be used to bypass pickle for saving
    large binary states.

    extraDataDir:
                  Model's extra data directory path
    """
    makeDirectoryFromAbsolutePath(extraDataDir)

    #--------------------------------------------------
    # Save the network
    outputDir = self.__getNetworkStateDirectory(extraDataDir=extraDataDir)

    self.__logger.debug("Serializing network...")

    self._netInfo.net.save(outputDir)

    self.__logger.debug("Finished serializing network")

    return