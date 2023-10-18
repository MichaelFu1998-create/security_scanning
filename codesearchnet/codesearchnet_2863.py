def make_shell_logfiles_url(host, shell_port, _, instance_id=None):
  """
  Make the url for log-files in heron-shell
  from the info stored in stmgr.
  If no instance_id is provided, the link will
  be to the dir for the whole container.
  If shell port is not present, it returns None.
  """
  if not shell_port:
    return None
  if not instance_id:
    return "http://%s:%d/browse/log-files" % (host, shell_port)
  else:
    return "http://%s:%d/file/log-files/%s.log.0" % (host, shell_port, instance_id)