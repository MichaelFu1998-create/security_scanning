def getInstancePid(topology_info, instance_id):
  """
  This method is used by other modules, and so it
  is not a part of the class.
  Fetches Instance pid from heron-shell.
  """
  try:
    http_client = tornado.httpclient.AsyncHTTPClient()
    endpoint = utils.make_shell_endpoint(topology_info, instance_id)
    url = "%s/pid/%s" % (endpoint, instance_id)
    Log.debug("HTTP call for url: %s", url)
    response = yield http_client.fetch(url)
    raise tornado.gen.Return(response.body)
  except tornado.httpclient.HTTPError as e:
    raise Exception(str(e))