def addInstance(self, groundTruth, prediction, record = None, result = None):
    """Compute and store metric value"""
    self.value = self.avg(prediction)