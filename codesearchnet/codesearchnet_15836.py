def detect_anomaly(self):
    """
    Detect anomalies in the timeseries data for the submetrics specified in the config file. Identified anomalies are
    stored in self.anomalies as well as written to .anomalies.csv file to be used by the client charting page. Anomaly
    detection uses the luminol library (http://pypi.python.org/pypi/luminol)
    """
    if not self.anomaly_detection_metrics or len(self.anomaly_detection_metrics) <= 0:
      return
    for submetric in self.anomaly_detection_metrics:
      csv_file = self.get_csv(submetric)
      if naarad.utils.is_valid_file(csv_file):
        detector = anomaly_detector.AnomalyDetector(csv_file)
        anomalies = detector.get_anomalies()
        if len(anomalies) <= 0:
          return
        self.anomalies[submetric] = anomalies
        anomaly_csv_file = os.path.join(self.resource_directory, self.label + '.' + submetric + '.anomalies.csv')
        with open(anomaly_csv_file, 'w') as FH:
          for anomaly in anomalies:
            FH.write(",".join([str(anomaly.anomaly_score), str(anomaly.start_timestamp), str(anomaly.end_timestamp), str(anomaly.exact_timestamp)]))
            FH.write('\n')