def stop_cluster(cl_args):
  '''
  teardown the cluster
  '''
  Log.info("Terminating cluster...")

  roles = read_and_parse_roles(cl_args)
  masters = roles[Role.MASTERS]
  slaves = roles[Role.SLAVES]
  dist_nodes = masters.union(slaves)

  # stop all jobs
  if masters:
    try:
      single_master = list(masters)[0]
      jobs = get_jobs(cl_args, single_master)
      for job in jobs:
        job_id = job["ID"]
        Log.info("Terminating job %s" % job_id)
        delete_job(cl_args, job_id, single_master)
    except:
      Log.debug("Error stopping jobs")
      Log.debug(sys.exc_info()[0])

  for node in dist_nodes:
    Log.info("Terminating processes on %s" % node)
    if not is_self(node):
      cmd = "ps aux | grep heron-nomad | awk '{print \$2}' " \
            "| xargs kill"
      cmd = ssh_remote_execute(cmd, node, cl_args)
    else:
      cmd = "ps aux | grep heron-nomad | awk '{print $2}' " \
            "| xargs kill"
    Log.debug(cmd)
    pid = subprocess.Popen(cmd,
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)

    return_code = pid.wait()
    output = pid.communicate()
    Log.debug("return code: %s output: %s" % (return_code, output))

    Log.info("Cleaning up directories on %s" % node)
    cmd = "rm -rf /tmp/slave ; rm -rf /tmp/master"
    if not is_self(node):
      cmd = ssh_remote_execute(cmd, node, cl_args)
    Log.debug(cmd)
    pid = subprocess.Popen(cmd,
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)

    return_code = pid.wait()
    output = pid.communicate()
    Log.debug("return code: %s output: %s" % (return_code, output))