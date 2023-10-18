def run(command, parser, cl_args, unknown_args):
  """ run command """
  try:
    clusters = tracker_access.get_clusters()
  except:
    Log.error("Fail to connect to tracker: \'%s\'", cl_args["tracker_url"])
    return False
  print('Available clusters:')
  for cluster in clusters:
    print('  %s' % cluster)
  return True