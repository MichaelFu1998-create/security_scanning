def __shouldSysExit(self, iteration):
    """
    Checks to see if the model should exit based on the exitAfter dummy
    parameter
    """

    if self._exitAfter is None \
       or iteration < self._exitAfter:
      return False

    results = self._jobsDAO.modelsGetFieldsForJob(self._jobID, ['params'])

    modelIDs = [e[0] for e in results]
    modelNums = [json.loads(e[1][0])['structuredParams']['__model_num'] for e in results]

    sameModelNumbers = filter(lambda x: x[1] == self.modelIndex,
                              zip(modelIDs, modelNums))

    firstModelID = min(zip(*sameModelNumbers)[0])

    return firstModelID == self._modelID