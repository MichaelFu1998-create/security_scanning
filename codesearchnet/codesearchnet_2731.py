def wait_for_job_to_start(single_master, job):
  '''
  Wait for a Nomad job to start
  '''
  i = 0
  while True:
    try:
      r = requests.get("http://%s:4646/v1/job/%s" % (single_master, job))
      if r.status_code == 200 and r.json()["Status"] == "running":
        break
      else:
        raise RuntimeError()
    except:
      Log.debug(sys.exc_info()[0])
      Log.info("Waiting for %s to come up... %s" % (job, i))
      time.sleep(1)
      if i > 20:
        Log.error("Failed to start Nomad Cluster!")
        sys.exit(-1)
    i = i + 1