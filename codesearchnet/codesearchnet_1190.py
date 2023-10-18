def anomalyGetLabels(self, start, end):
    """
    Get labels from the anomaly classifier within this model.

    :param start: (int) index to start getting labels
    :param end: (int) index to end getting labels
    """
    return self._getAnomalyClassifier().getSelf().getLabels(start, end)