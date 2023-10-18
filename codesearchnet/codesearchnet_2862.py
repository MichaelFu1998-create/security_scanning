def make_shell_endpoint(topologyInfo, instance_id):
  """
  Makes the http endpoint for the heron shell
  if shell port is present, otherwise returns None.
  """
  # Format: container_<id>_<instance_id>
  pplan = topologyInfo["physical_plan"]
  stmgrId = pplan["instances"][instance_id]["stmgrId"]
  host = pplan["stmgrs"][stmgrId]["host"]
  shell_port = pplan["stmgrs"][stmgrId]["shell_port"]
  return "http://%s:%d" % (host, shell_port)