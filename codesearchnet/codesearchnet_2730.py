def wait_for_master_to_start(single_master):
  '''
  Wait for a nomad master to start
  '''
  i = 0
  while True:
    try:
      r = requests.get("http://%s:4646/v1/status/leader" % single_master)
      if r.status_code == 200:
        break
    except:
      Log.debug(sys.exc_info()[0])
      Log.info("Waiting for cluster to come up... %s" % i)
      time.sleep(1)
      if i > 10:
        Log.error("Failed to start Nomad Cluster!")
        sys.exit(-1)
    i = i + 1