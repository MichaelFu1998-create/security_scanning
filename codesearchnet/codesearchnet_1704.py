def addSynapse(self, srcCellCol, srcCellIdx, perm):
    """Add a new synapse

    :param srcCellCol source cell column
    :param srcCellIdx source cell index within the column
    :param perm       initial permanence
    """
    self.syns.append([int(srcCellCol), int(srcCellIdx), numpy.float32(perm)])