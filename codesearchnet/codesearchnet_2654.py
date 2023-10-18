def getComponentMetrics(self,
                          tmaster,
                          componentName,
                          metricNames,
                          instances,
                          interval,
                          callback=None):
    """
    Get the specified metrics for the given component name of this topology.
    Returns the following dict on success:
    {
      "metrics": {
        <metricname>: {
          <instance>: <numeric value>,
          <instance>: <numeric value>,
          ...
        }, ...
      },
      "interval": <numeric value>,
      "component": "..."
    }

    Raises exception on failure.
    """
    if not tmaster or not tmaster.host or not tmaster.stats_port:
      raise Exception("No Tmaster found")

    host = tmaster.host
    port = tmaster.stats_port

    metricRequest = tmaster_pb2.MetricRequest()
    metricRequest.component_name = componentName
    if len(instances) > 0:
      for instance in instances:
        metricRequest.instance_id.append(instance)
    for metricName in metricNames:
      metricRequest.metric.append(metricName)
    metricRequest.interval = interval

    # Serialize the metricRequest to send as a payload
    # with the HTTP request.
    metricRequestString = metricRequest.SerializeToString()

    url = "http://{0}:{1}/stats".format(host, port)
    request = tornado.httpclient.HTTPRequest(url,
                                             body=metricRequestString,
                                             method='POST',
                                             request_timeout=5)

    Log.debug("Making HTTP call to fetch metrics")
    Log.debug("url: " + url)
    try:
      client = tornado.httpclient.AsyncHTTPClient()
      result = yield client.fetch(request)
      Log.debug("HTTP call complete.")
    except tornado.httpclient.HTTPError as e:
      raise Exception(str(e))

    # Check the response code - error if it is in 400s or 500s
    responseCode = result.code
    if responseCode >= 400:
      message = "Error in getting metrics from Tmaster, code: " + responseCode
      Log.error(message)
      raise Exception(message)

    # Parse the response from tmaster.
    metricResponse = tmaster_pb2.MetricResponse()
    metricResponse.ParseFromString(result.body)

    if metricResponse.status.status == common_pb2.NOTOK:
      if metricResponse.status.HasField("message"):
        Log.warn("Received response from Tmaster: %s", metricResponse.status.message)

    # Form the response.
    ret = {}
    ret["interval"] = metricResponse.interval
    ret["component"] = componentName
    ret["metrics"] = {}
    for metric in metricResponse.metric:
      instance = metric.instance_id
      for im in metric.metric:
        metricname = im.name
        value = im.value
        if metricname not in ret["metrics"]:
          ret["metrics"][metricname] = {}
        ret["metrics"][metricname][instance] = value

    raise tornado.gen.Return(ret)