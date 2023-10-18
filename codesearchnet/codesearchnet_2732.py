def scp_package(package_file, destinations, cl_args):
  '''
  scp and extract package
  '''
  pids = []
  for dest in destinations:
    if is_self(dest):
      continue
    Log.info("Server: %s" % dest)
    file_path = "/tmp/heron.tar.gz"
    dest_file_path = "%s:%s" % (dest, file_path)

    remote_cmd = "rm -rf ~/.heron && mkdir ~/.heron " \
                 "&& tar -xzvf %s -C ~/.heron --strip-components 1" % (file_path)
    cmd = '%s && %s' \
          % (scp_cmd(package_file, dest_file_path, cl_args),
             ssh_remote_execute(remote_cmd, dest, cl_args))
    Log.debug(cmd)
    pid = subprocess.Popen(cmd,
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    pids.append({"pid": pid, "dest": dest})

  errors = []
  for entry in pids:
    pid = entry["pid"]
    return_code = pid.wait()
    output = pid.communicate()
    Log.debug("return code: %s output: %s" % (return_code, output))
    if return_code != 0:
      errors.append("Failed to scp package to %s with error:\n%s" % (entry["dest"], output[1]))

  if errors:
    for error in errors:
      Log.error(error)
    sys.exit(-1)

  Log.info("Done distributing packages")