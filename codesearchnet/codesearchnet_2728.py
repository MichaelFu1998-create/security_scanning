def start_heron_tools(masters, cl_args):
  '''
  Start Heron tracker and UI
  '''
  single_master = list(masters)[0]
  wait_for_master_to_start(single_master)

  cmd = "%s run %s >> /tmp/heron_tools_start.log 2>&1 &" \
        % (get_nomad_path(cl_args), get_heron_tools_job_file(cl_args))
  Log.info("Starting Heron Tools on %s" % single_master)

  if not is_self(single_master):
    cmd = ssh_remote_execute(cmd, single_master, cl_args)
  Log.debug(cmd)
  pid = subprocess.Popen(cmd,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

  return_code = pid.wait()
  output = pid.communicate()
  Log.debug("return code: %s output: %s" % (return_code, output))
  if return_code != 0:
    Log.error("Failed to start Heron Tools on %s with error:\n%s" % (single_master, output[1]))
    sys.exit(-1)

  wait_for_job_to_start(single_master, "heron-tools")
  Log.info("Done starting Heron Tools")