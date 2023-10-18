def _translateMetricsToJSON(self, metrics, label):
    """ Translates the given metrics value to JSON string

    metrics:        A list of dictionaries per OPFTaskDriver.getMetrics():

    Returns:        JSON string representing the given metrics object.
    """

    # Transcode the MetricValueElement values into JSON-compatible
    # structure
    metricsDict = metrics

    # Convert the structure to a display-friendly JSON string
    def _mapNumpyValues(obj):
      """
      """
      import numpy

      if isinstance(obj, numpy.float32):
        return float(obj)

      elif isinstance(obj, numpy.bool_):
        return bool(obj)

      elif isinstance(obj, numpy.ndarray):
        return obj.tolist()

      else:
        raise TypeError("UNEXPECTED OBJ: %s; class=%s" % (obj, obj.__class__))


    jsonString = json.dumps(metricsDict, indent=4, default=_mapNumpyValues)

    return jsonString