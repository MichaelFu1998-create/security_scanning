def start_master_nodes(masters, cl_args):
  '''
  Start master nodes
  '''
  pids = []
  for master in masters:
    Log.info("Starting master on %s" % master)
    cmd = "%s agent -config %s >> /tmp/nomad_server_log 2>&1 &" \
          % (get_nomad_path(cl_args), get_nomad_master_config_file(cl_args))
    if not is_self(master):
      cmd = ssh_remote_execute(cmd, master, cl_args)
    Log.debug(cmd)
    pid = subprocess.Popen(cmd,
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    pids.append({"pid": pid, "dest": master})

  errors = []
  for entry in pids:
    pid = entry["pid"]
    return_code = pid.wait()
    output = pid.communicate()
    Log.debug("return code: %s output: %s" % (return_code, output))
    if return_code != 0:
      errors.append("Failed to start master on %s with error:\n%s" % (entry["dest"], output[1]))

  if errors:
    for error in errors:
      Log.error(error)
    sys.exit(-1)

  Log.info("Done starting masters")