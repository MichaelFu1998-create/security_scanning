def anomalyRemoveLabels(self, start, end, labelFilter):
    """
    Remove labels from the anomaly classifier within this model. Removes all
    records if ``labelFilter==None``, otherwise only removes the labels equal to
    ``labelFilter``.

    :param start: (int) index to start removing labels
    :param end: (int) index to end removing labels
    :param labelFilter: (string) If specified, only removes records that match
    """
    self._getAnomalyClassifier().getSelf().removeLabels(start, end, labelFilter)