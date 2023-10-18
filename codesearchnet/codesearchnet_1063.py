def _createPredictionLogger(self):
    """
    Creates the model's PredictionLogger object, which is an interface to write
    model results to a permanent storage location
    """

    class DummyLogger:
      def writeRecord(self, record): pass
      def writeRecords(self, records, progressCB): pass
      def close(self): pass

    self._predictionLogger = DummyLogger()