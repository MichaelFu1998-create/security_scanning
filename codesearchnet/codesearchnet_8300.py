def getOperationNameForId(self, i):
        """ Convert an operation id into the corresponding string
        """
        for key in self.ops:
            if int(self.ops[key]) is int(i):
                return key
        raise ValueError("Unknown Operation ID %d" % i)