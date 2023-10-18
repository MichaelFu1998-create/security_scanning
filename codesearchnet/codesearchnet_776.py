def _classifyState(self, state):
    """
    Reclassifies given state.
    """
    # Record is before wait period do not classifiy
    if state.ROWID < self.getParameter('trainRecords'):
      if not state.setByUser:
        state.anomalyLabel = []
        self._deleteRecordsFromKNN([state])
      return

    label = KNNAnomalyClassifierRegion.AUTO_THRESHOLD_CLASSIFIED_LABEL
    autoLabel = label + KNNAnomalyClassifierRegion.AUTO_TAG

    # Update the label based on classifications
    newCategory = self._recomputeRecordFromKNN(state)
    labelList = self._categoryToLabelList(newCategory)

    if state.setByUser:
      if label in state.anomalyLabel:
        state.anomalyLabel.remove(label)
      if autoLabel in state.anomalyLabel:
        state.anomalyLabel.remove(autoLabel)
      labelList.extend(state.anomalyLabel)

    # Add threshold classification label if above threshold, else if
    # classified to add the auto threshold classification.
    if state.anomalyScore >= self.getParameter('anomalyThreshold'):
      labelList.append(label)
    elif label in labelList:
      ind = labelList.index(label)
      labelList[ind] = autoLabel

    # Make all entries unique
    labelList = list(set(labelList))

    # If both above threshold and auto classified above - remove auto label
    if label in labelList and autoLabel in labelList:
      labelList.remove(autoLabel)

    if state.anomalyLabel == labelList:
      return

    # Update state's labeling
    state.anomalyLabel = labelList

    # Update KNN Classifier with new labeling
    if state.anomalyLabel == []:
      self._deleteRecordsFromKNN([state])
    else:
      self._addRecordToKNN(state)