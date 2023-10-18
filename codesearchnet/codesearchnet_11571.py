def getVector(self, tree, branchName):
        """return the ROOT.vector object for the branch.

        """

        if (tree, branchName) in self.__class__.addressDict:
            return self.__class__.addressDict[(tree, branchName)]

        itsVector = self._getVector(tree, branchName)
        self.__class__.addressDict[(tree, branchName)] = itsVector

        return itsVector