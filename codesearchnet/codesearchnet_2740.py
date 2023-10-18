def get_hostname(ip_addr, cl_args):
  '''
  get host name of remote host
  '''
  if is_self(ip_addr):
    return get_self_hostname()
  cmd = "hostname"
  ssh_cmd = ssh_remote_execute(cmd, ip_addr, cl_args)
  pid = subprocess.Popen(ssh_cmd,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
  return_code = pid.wait()
  output = pid.communicate()

  if return_code != 0:
    Log.error("Failed to get hostname for remote host %s with output:\n%s" % (ip_addr, output))
    sys.exit(-1)
  return output[0].strip("\n")