def getStmgrsRegSummary(self, tmaster, callback=None):
    """
    Get summary of stream managers registration summary
    """
    if not tmaster or not tmaster.host or not tmaster.stats_port:
      return
    reg_request = tmaster_pb2.StmgrsRegistrationSummaryRequest()
    request_str = reg_request.SerializeToString()
    port = str(tmaster.stats_port)
    host = tmaster.host
    url = "http://{0}:{1}/stmgrsregistrationsummary".format(host, port)
    request = tornado.httpclient.HTTPRequest(url,
                                             body=request_str,
                                             method='POST',
                                             request_timeout=5)
    Log.debug('Making HTTP call to fetch stmgrsregistrationsummary url: %s', url)
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
    reg_response = tmaster_pb2.StmgrsRegistrationSummaryResponse()
    reg_response.ParseFromString(result.body)
    # Send response
    ret = {}
    for stmgr in reg_response.registered_stmgrs:
      ret[stmgr] = True
    for stmgr in reg_response.absent_stmgrs:
      ret[stmgr] = False
    raise tornado.gen.Return(ret)