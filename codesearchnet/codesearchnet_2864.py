def make_shell_logfile_data_url(host, shell_port, instance_id, offset, length):
  """
  Make the url for log-file data in heron-shell
  from the info stored in stmgr.
  """
  return "http://%s:%d/filedata/log-files/%s.log.0?offset=%s&length=%s" % \
    (host, shell_port, instance_id, offset, length)