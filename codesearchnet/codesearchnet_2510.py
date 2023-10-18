def getComponentExceptionSummary(self, tmaster, component_name, instances=[], callback=None):
    """
    Get the summary of exceptions for component_name and list of instances.
    Empty instance list will fetch all exceptions.
    """
    if not tmaster or not tmaster.host or not tmaster.stats_port:
      return
    exception_request = tmaster_pb2.ExceptionLogRequest()
    exception_request.component_name = component_name
    if len(instances) > 0:
      exception_request.instances.extend(instances)
    request_str = exception_request.SerializeToString()
    port = str(tmaster.stats_port)
    host = tmaster.host
    url = "http://{0}:{1}/exceptionsummary".format(host, port)
    Log.debug("Creating request object.")
    request = tornado.httpclient.HTTPRequest(url,
                                             body=request_str,
                                             method='POST',
                                             request_timeout=5)
    Log.debug('Making HTTP call to fetch exceptionsummary url: %s', url)
    try:
      client = tornado.httpclient.AsyncHTTPClient()
      result = yield client.fetch(request)
      Log.debug("HTTP call complete.")
    except tornado.httpclient.HTTPError as e:
      raise Exception(str(e))

    # Check the response code - error if it is in 400s or 500s
    responseCode = result.code
    if responseCode >= 400:
      message = "Error in getting exceptions from Tmaster, code: " + responseCode
      Log.error(message)
      raise tornado.gen.Return({
          "message": message
      })

    # Parse the response from tmaster.
    exception_response = tmaster_pb2.ExceptionLogResponse()
    exception_response.ParseFromString(result.body)

    if exception_response.status.status == common_pb2.NOTOK:
      if exception_response.status.HasField("message"):
        raise tornado.gen.Return({
            "message": exception_response.status.message
        })

    # Send response
    ret = []
    for exception_log in exception_response.exceptions:
      ret.append({'class_name': exception_log.stacktrace,
                  'lasttime': exception_log.lasttime,
                  'firsttime': exception_log.firsttime,
                  'count': str(exception_log.count)})
    raise tornado.gen.Return(ret)