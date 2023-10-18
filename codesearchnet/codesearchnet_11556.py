def getArrays(self, tree, branchName):
        """return the array.array objects for the branch and its counter branch

        This method returns a pair of the array.array objects. The first one is
        for the given tree and branch name. The second one is for its counter
        branch. The second one will be None when the branch does not have a
        counter. A pair of None will be returned when the tree does not have
        the branch.

        """
        itsArray = self._getArray(tree, branchName)
        if itsArray is None: return None, None
        itsCountArray = self._getCounterArray(tree, branchName)
        return itsArray, itsCountArray