def _addPartitionId(self, index, partitionId=None):
    """
    Adds partition id for pattern index
    """
    if partitionId is None:
      self._partitionIdList.append(numpy.inf)
    else:
      self._partitionIdList.append(partitionId)
      indices = self._partitionIdMap.get(partitionId, [])
      indices.append(index)
      self._partitionIdMap[partitionId] = indices