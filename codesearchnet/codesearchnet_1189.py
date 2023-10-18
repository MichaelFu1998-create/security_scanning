def anomalyAddLabel(self, start, end, labelName):
    """
    Add labels from the anomaly classifier within this model.

    :param start: (int) index to start label
    :param end: (int) index to end label
    :param labelName: (string) name of label
    """
    self._getAnomalyClassifier().getSelf().addLabel(start, end, labelName)