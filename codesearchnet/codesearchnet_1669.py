def printParameters(self):
    """
    Print the parameter settings for the TM.
    """
    print "numberOfCols=", self.numberOfCols
    print "cellsPerColumn=", self.cellsPerColumn
    print "minThreshold=", self.minThreshold
    print "newSynapseCount=", self.newSynapseCount
    print "activationThreshold=", self.activationThreshold
    print
    print "initialPerm=", self.initialPerm
    print "connectedPerm=", self.connectedPerm
    print "permanenceInc=", self.permanenceInc
    print "permanenceDec=", self.permanenceDec
    print "permanenceMax=", self.permanenceMax
    print "globalDecay=", self.globalDecay
    print
    print "doPooling=", self.doPooling
    print "segUpdateValidDuration=", self.segUpdateValidDuration
    print "pamLength=", self.pamLength