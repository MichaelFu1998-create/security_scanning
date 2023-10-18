def getInstanceJstack(self, topology_info, instance_id):
    """
    Fetches Instance jstack from heron-shell.
    """
    pid_response = yield getInstancePid(topology_info, instance_id)
    try:
      http_client = tornado.httpclient.AsyncHTTPClient()
      pid_json = json.loads(pid_response)
      pid = pid_json['stdout'].strip()
      if pid == '':
        raise Exception('Failed to get pid')
      endpoint = utils.make_shell_endpoint(topology_info, instance_id)
      url = "%s/jstack/%s" % (endpoint, pid)
      response = yield http_client.fetch(url)
      Log.debug("HTTP call for url: %s", url)
      raise tornado.gen.Return(response.body)
    except tornado.httpclient.HTTPError as e:
      raise Exception(str(e))