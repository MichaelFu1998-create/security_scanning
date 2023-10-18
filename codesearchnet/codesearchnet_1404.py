def _rebuildPartitionIdMap(self, partitionIdList):
    """
    Rebuilds the partition Id map using the given partitionIdList
    """
    self._partitionIdMap = {}
    for row, partitionId in enumerate(partitionIdList):
      indices = self._partitionIdMap.get(partitionId, [])
      indices.append(row)
      self._partitionIdMap[partitionId] = indices