def get_remote_home(host, cl_args):
  '''
  get home directory of remote host
  '''
  cmd = "echo ~"
  if not is_self(host):
    cmd = ssh_remote_execute(cmd, host, cl_args)
  pid = subprocess.Popen(cmd,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
  return_code = pid.wait()
  output = pid.communicate()

  if return_code != 0:
    Log.error("Failed to get home path for remote host %s with output:\n%s" % (host, output))
    sys.exit(-1)
  return output[0].strip("\n")