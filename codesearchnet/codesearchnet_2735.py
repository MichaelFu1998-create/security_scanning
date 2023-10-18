def start_slave_nodes(slaves, cl_args):
  '''
  Star slave nodes
  '''
  pids = []
  for slave in slaves:
    Log.info("Starting slave on %s" % slave)
    cmd = "%s agent -config %s >> /tmp/nomad_client.log 2>&1 &" \
          % (get_nomad_path(cl_args), get_nomad_slave_config_file(cl_args))
    if not is_self(slave):
      cmd = ssh_remote_execute(cmd, slave, cl_args)
    Log.debug(cmd)
    pid = subprocess.Popen(cmd,
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    pids.append({"pid": pid, "dest": slave})

  errors = []
  for entry in pids:
    pid = entry["pid"]
    return_code = pid.wait()
    output = pid.communicate()
    Log.debug("return code: %s output: %s" % (return_code, output))
    if return_code != 0:
      errors.append("Failed to start slave on %s with error:\n%s" % (entry["dest"], output[1]))

  if errors:
    for error in errors:
      Log.error(error)
    sys.exit(-1)

  Log.info("Done starting slaves")