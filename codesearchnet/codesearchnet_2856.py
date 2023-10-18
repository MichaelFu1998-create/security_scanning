def get(self):
    """ get method """
    try:
      cluster = self.get_argument_cluster()
      role = self.get_argument_role()
      environ = self.get_argument_environ()
      topology_name = self.get_argument_topology()
      container = self.get_argument(constants.PARAM_CONTAINER)
      path = self.get_argument(constants.PARAM_PATH)
      offset = self.get_argument_offset()
      length = self.get_argument_length()
      topology_info = self.tracker.getTopologyInfo(topology_name, cluster, role, environ)

      stmgr_id = "stmgr-" + container
      stmgr = topology_info["physical_plan"]["stmgrs"][stmgr_id]
      host = stmgr["host"]
      shell_port = stmgr["shell_port"]
      file_data_url = "http://%s:%d/filedata/%s?offset=%s&length=%s" % \
        (host, shell_port, path, offset, length)

      http_client = tornado.httpclient.AsyncHTTPClient()
      response = yield http_client.fetch(file_data_url)
      self.write_success_response(json.loads(response.body))
      self.finish()
    except Exception as e:
      Log.debug(traceback.format_exc())
      self.write_error_response(e)