def post(self):
    """ post method """
    def status_finish(ret):
      self.set_status(ret)
      self.finish()

    def kill_parent():
      status_finish(200)
      logger.info("Killing parent executor")
      os.killpg(os.getppid(), signal.SIGTERM)

    logger = logging.getLogger(__file__)
    logger.info("Received 'Killing process' request")
    data = dict(urlparse.parse_qsl(self.request.body))

    # check shared secret
    sharedSecret = data.get('secret')
    if sharedSecret != options.secret:
      status_finish(403)
      return

    instanceId = data.get('instance_id_to_restart')
    if instanceId:
      filepath = instanceId + '.pid'
      if os.path.isfile(filepath): # instance_id found
        if instanceId.startswith('heron-executor-'): # kill heron-executor
          kill_parent()
        else: # kill other normal instance
          fh = open(filepath)
          firstLine = int(fh.readline())
          fh.close()
          logger.info("Killing process " + instanceId + " " + str(firstLine))
          os.kill(firstLine, signal.SIGTERM)
          status_finish(200)
      else: # instance_id not found
        logger.info(filepath + " not found")
        status_finish(422)
    else: # instance_id not given, which means kill the container
      kill_parent()